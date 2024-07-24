def get_proper_serializer(view, request):
    if request is None:
        return view.basic_serializer_class
    serializer_class = request.query_params.get("serializer", False)
    if serializer_class == "aggregated" and view.aggregated_serializer_class is not None:
        return view.aggregated_serializer_class
    return view.basic_serializer_class
