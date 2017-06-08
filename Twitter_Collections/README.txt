*Contains jar files for processing Tweet streaming.
*For example, lots of instances of duplicate Tweets would occur, so we handled that.
*We also replaced ticker names of companes (e.g., INTC) with their actual company names (e.g., Intel) for our actual analysis,
so that all Intel tweets would be identified as such.
*We also had to pair Tweets with their respective financial data - we have a lag time of 2 days currently implemented, so Tweets
are paired with stock movement for 2 days into the future.
