
from eventregistry import *
er = EventRegistry()
q = QueryEvents()
# get events related to Barack Obama
q.addConcept(er.getConceptUri("Boeing"))
# that have been reported also by BBC

# return event details for largest 30 events
q.addRequestedResult(RequestEventsInfo(page = 1, count = 1, sortBy = "size", sortByAsc = False))   
# return top 5 locations and organizations mentioned the most in these events

      
# execute the query
print er.execQuery(q)
