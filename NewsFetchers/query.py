from eventregistry import *
er = EventRegistry()
q = QueryEvents()
q.addConcept(er.getConceptUri("Star Wars"))   
q.addRequestedResult(RequestEventsInfo(sortBy = "date", count=10))   # return event details for last 10 events
print er.execQuery(q)
