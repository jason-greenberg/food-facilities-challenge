build tables: alembic upgrade head

seed command: python -m db.seeds.seed seed
undo seed command: python -m db.seeds.seed undo

## Decision: Implementing Geospatial Search Using the Haversine Formula Over PostGIS
One of the key features of my application was the ability to find the five nearest food trucks based on a given latitude and longitude. Implementing geospatial querying can be complex, and there are two main ways to achieve it:

1. PostGIS: PostGIS is an extension for PostgreSQL that can transform the database into a spatial database system, allowing advanced geospatial queries directly from the database.

2. Haversine Formula: The Haversine Formula is an equation that calculates the shortest distance between two points on the surface of a sphere, given their longitudes and latitudes.

I decided to use the Haversine Formula for the following reasons:

- Simplicity: The Haversine formula provides a simple and efficient way to calculate the distances between latitude-longitude pairs. I could implement this formula directly in my code without having to rely on external libraries or database extensions, which I felt would keep my codebase more manageable.

- Less Learning Overhead: While PostGIS is powerful, it does have a steep learning curve and requires considerable setup to integrate into a project. Given my limited time frame and the scale of this project, I felt it was more practical to use a solution that I could implement and understand quickly.

- No Additional Dependencies: By using the Haversine Formula instead of PostGIS, I avoided introducing another dependency to the project. This reduces potential points of failure and makes the application more portable and easier to set up.

- Understanding Scalability Trade-Offs: While the Haversine Formula was suitable for my use case, I understand that it might not be the best solution for larger applications with more data and complex geospatial querying requirements. A dedicated solution like PostGIS could be more efficient for those scenarios. However, considering the current requirements and data size of this project, the Haversine formula offered a satisfactory solution.

In conclusion, the choice to use the Haversine Formula was a trade-off based on the current scope of the project, time constraints, and my desire to keep the solution as simple and manageable as possible. For a larger, more complex application, a tool like PostGIS would be a more fitting choice for advanced and efficient geospatial querying.
