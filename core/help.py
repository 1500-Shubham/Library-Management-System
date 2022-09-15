class TravelDelegate(View):

    def __init__(self):
        self.response = init_response()
        self.LONG_FUTURE_DATE = datetime.strptime('2047-08-15', '%Y-%m-%d')  # CONSTANT long future date for unlimited expiry

    def format_date(self, params):
        if params.get('from_date'):
            from_d = datetime.strptime(params.get('from_date'), '%Y-%m-%d')
        else:
            from_d = None

        if params.get('to_date'):
            to_d = datetime.strptime(params.get('to_date'), '%Y-%m-%d')
        else:
            to_d = None
        return from_d, to_d

    @decorator_4xx(['delegation_type'])
    def get(self, request):
        params = request.GET
        user = request.user
        happay_id = request.GET.get('happay_id')
        if happay_id:
            user = HappayUser.objects.get(pk=happay_id)

        delegation_type = params.get('delegation_type')
        if delegation_type == 'delegator':
            delegated_users = TDelegatedUser.objects.filter(delegator=user, status=True).order_by("-from_date")
        if delegation_type == 'delegated':
            delegated_users = TDelegatedUser.objects.filter(delegated=user, status=True).order_by("-from_date")
        self.response['res_data'] = TDelegatedUser.serializer(delegated_users)
        return send_200(self.response)

    @decorator_4xx(['delegated', 'from_date'])
    def post(self, request):
        data = request.POST
        delegator = request.user
        delegated_users = json.loads(data.get('delegated'))
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        till_delete = data.get('till_delete')
        from_date, to_date = self.format_date(data)
        delegation_id  = data.get('delegation_id')

        # when delegation expiry is unlimited/until deleted
        if till_delete and not to_date:
            to_date = self.LONG_FUTURE_DATE

        try:
            if delegator.pk in delegated_users:
                raise AssertionError("Delegator can not be delegated")

            delegated_objs = []
            for delg_uid in delegated_users:
                delegated = HappayUser.objects.get(pk=delg_uid)

                if delegation_id:
                    t_delg_obj = TDelegatedUser.objects.get(pk=delegation_id)
                    t_delg_obj.delegated = delegated
                else:
                    t_delg_obj = TDelegatedUser(delegator=delegator, delegated=delegated)
                if from_date and to_date:
                    t_delg_obj.from_date = from_date
                    t_delg_obj.to_date = to_date
                t_delg_obj.reason = data.get('reason')
                delegated_objs.append(t_delg_obj)

            with transaction.atomic():
                if delegation_id:
                    TDelegatedUser.objects.bulk_update(delegated_objs)
                else:
                    TDelegatedUser.objects.bulk_create(delegated_objs)
            # notify delegated user

        except Exception as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)

        self.response['res_str'] = "Delegated created successfully"
        return send_201(self.response)


    @decorator_4xx(['delegation_id'])
    def delete(self, request):
        delegator = request.user
        params = QueryDict(request.body)
        delegation_id = params.get('delegation_id')
        try:
            if delegator:
                delg_obj = TDelegatedUser.objects.get(pk=delegation_id)
                if delg_obj.delegator.pk == delegator.pk:
                    delg_obj.status = False
                    delg_obj.save()
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)
        self.response['res_str'] = "Delegated deleted successfully"
        return send_200(self.response)