class PostFields:
    def setPostFields(self, plainTextList, photoList, dateList, selectionList, documentList, eventList, priceList, locationList ):
        if plainTextList:
            self.plainTextList =plainTextList
        if photoList:
            self.photoList = photoList
        if dateList:
            self.dateList = dateList
        if selectionList:
            self.selectionList = selectionList
        if documentList:
            self.documentList = documentList
        if eventList:
            self.eventList = eventList
        if priceList:
            self.priceList = priceList
        if locationList:
            self.locationList = locationList

        return 0
