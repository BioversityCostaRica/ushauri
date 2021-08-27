from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ushauri.processes.db.maintenance import (
    getRegions,
    addCounty,
    deleteCounty,
    getCountyData,
    updateCounty,
    getSubCounties2,
    getCountyName,
    addSubCounty,
    deleteSubCounty,
    getSubCountyData,
    updateSubCounty,
)
from ushauri.views.classes import privateView


class countiesList_view(privateView):
    def processView(self):
        regions = getRegions(self.request)
        return {"regions": regions}


class addCounty_view(privateView):
    def processView(self):
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["county_name"] != "":
                    added, message = addCounty(self.request, data["county_name"])
                    if added:
                        return HTTPFound(location=self.request.route_url("counties"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["county_name"] = "The name cannot be empty"

        return {"error_summary": error_summary, "data": data}


class modifyCounty_view(privateView):
    def processView(self):
        county = self.request.matchdict["county"]
        error_summary = {}
        data = getCountyData(self.request, county)
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                if data["county_name"] != "":
                    update, message = updateCounty(
                        self.request, county, data["county_name"]
                    )
                    if update:
                        return HTTPFound(location=self.request.route_url("counties"))
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["county_name"] = "The name cannot be empty"

        return {"error_summary": error_summary, "data": data}


class deleteCounty_view(privateView):
    def processView(self):
        county = self.request.matchdict["county"]
        if self.request.method == "POST":
            deleteCounty(self.request, county)
            return HTTPFound(location=self.request.route_url("counties"))
        else:
            raise HTTPNotFound


# ------------------------------/Sub counties ------------------------


class subCountiesList_view(privateView):
    def processView(self):
        countyID = self.request.matchdict["county"]
        countyName = getCountyName(self.request, countyID)
        subcounties = getSubCounties2(self.request, countyID)
        return {
            "subcounties": subcounties,
            "countyid": countyID,
            "countyname": countyName,
        }


class addSubCounty_view(privateView):
    def processView(self):
        countyID = self.request.matchdict["county"]
        countyName = getCountyName(self.request, countyID)
        error_summary = {}
        data = {}
        if self.request.method == "POST":
            if "add" in self.request.POST:
                data = self.getPostDict()
                if data["subcounty_name"] != "":
                    added, message = addSubCounty(
                        self.request, countyID, data["subcounty_name"]
                    )
                    if added:
                        return HTTPFound(
                            location=self.request.route_url(
                                "subcounties", county=countyID
                            )
                        )
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["county_name"] = "The name cannot be empty"
        return {
            "error_summary": error_summary,
            "data": data,
            "countyid": countyID,
            "countyname": countyName,
        }


class deleteSubCounty_view(privateView):
    def processView(self):
        county = self.request.matchdict["county"]
        subCounty = self.request.matchdict["subcounty"]
        if self.request.method == "POST":
            deleteSubCounty(self.request, county, subCounty)
            return HTTPFound(
                location=self.request.route_url("subcounties", county=county)
            )
        else:
            raise HTTPNotFound


class editSubCounty_view(privateView):
    def processView(self):
        countyID = self.request.matchdict["county"]
        subCounty = self.request.matchdict["subcounty"]
        countyName = getCountyName(self.request, countyID)
        error_summary = {}
        data = getSubCountyData(self.request, countyID, subCounty)
        if self.request.method == "POST":
            if "edit" in self.request.POST:
                data = self.getPostDict()
                if data["subcounty_name"] != "":
                    updated, message = updateSubCounty(
                        self.request, countyID, subCounty, data["subcounty_name"]
                    )
                    if updated:
                        return HTTPFound(
                            location=self.request.route_url(
                                "subcounties", county=countyID
                            )
                        )
                    else:
                        error_summary["error"] = message
                else:
                    error_summary["county_name"] = self._("The name cannot be empty")
        return {
            "error_summary": error_summary,
            "data": data,
            "countyid": countyID,
            "countyname": countyName,
        }
