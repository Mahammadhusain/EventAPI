# SQL query to get top 3 events by total tickets sold

query = """
    SELECT 
        e.id, 
        e.name, 
        e.date, 
        e.total_tickets, 
        e.tickets_sold,
        COALESCE(SUM(t.quantity), 0) AS total_tickets_sold
    FROM 
        api_event AS e
    LEFT JOIN 
        api_ticket AS t
        ON e.id = t.event_id
    GROUP BY 
        e.id, e.name, e.date, e.total_tickets
    ORDER BY 
        total_tickets_sold DESC
    LIMIT 3;
"""

# =============== Query explanation ==================


# --------------
# Query part - 1
# --------------

"""
SELECT 
    e.id, 
    e.name, 
    e.date, 
    e.total_tickets, 
    e.tickets_sold,
    COALESCE(SUM(t.quantity), 0) AS total_tickets_sold
FROM 
    api_event AS e
"""
# Fetch data fields from api_event table and COALESCE(SUM(t.quantity), 0) AS total_tickets_sold: This calculates the total number of tickets sold for each event. It uses the SUM function to add up the quantities of tickets sold, and COALESCE ensures that if there are no tickets sold (i.e., the sum is NULL), it will return 0 instead.

# --------------
# Query part - 2
# --------------
"""
LEFT JOIN 
    api_ticket AS t
    ON e.id = t.event_id
"""
# The LEFT JOIN clause joins the api_ticket table (aliased as t) with the api_event table based on the condition that the event_id in the api_ticket table matches the id in the api_event table. A LEFT JOIN ensures that all records from the left table (api_event) are returned, along with matching records from the right table (api_ticket). If there are no matches in the api_ticket table, the result will still include the event, with NULL values for the ticket columns.

# --------------
# Query part - 3
# --------------
"""
GROUP BY 
    e.id, e.name, e.date, e.total_tickets
"""
# The GROUP BY clause groups the results by the specified columns. In this case, it groups the results by the event's id, name, date, and total_tickets. This is necessary because we are using aggregate functions (like SUM) in the SELECT clause.

# --------------
# Query part - 4
# --------------
"""
ORDER BY 
    total_tickets_sold DESC
"""
# The ORDER BY clause sorts the results based on the total_tickets_sold in descending order (DESC). This means that the events with the highest number of tickets sold will appear first in the result set.

# --------------
# Query part - 5
# --------------
"""
LIMIT 3;
"""

# Finally, the LIMIT 3 clause restricts the results to only the top 3 events based on the number of tickets sold. This is useful for retrieving a smaller, manageable set of data, especially when dealing with large datasets.