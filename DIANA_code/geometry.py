import matplotlib.pyplot as plt

def create_named_point_group(name, *points):
    """
    Groups given points into a dictionary under a specified name.
    
    Parameters:
    - name (str): The name of the group.
    - *points: Variable number of 2D point lists (e.g., Point_A, Point_B, ...)

    Returns:
    - dict: { name: [point1, point2, ...] }
    """
    return {name: list(points)}

def plot_filled_polygon(polygon_dict):
    """
    Plots and fills a polygon based on the points in a dictionary,
    with the polygon's name placed in the center.
    
    Parameters:
    - polygon_dict (dict): Dictionary with name as key and list of points as value.
    """
    for name, points in polygon_dict.items():
        # Unzip the list of points into X and Y coordinates
        x_coords, y_coords = zip(*points)
        
        # Close the shape by connecting the last point to the first point
        x_coords += (x_coords[0],)
        y_coords += (y_coords[0],)
        
        # Plot and fill the polygon
        plt.fill(x_coords, y_coords, color='skyblue', edgecolor='black', linewidth=2, alpha=0.5)
        
        # Calculate the centroid (center) of the polygon
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        # Place the name in the center of the polygon
        plt.text(center_x, center_y, name, fontsize=9, ha='center', color='black')

def plot_geometry(named_points, polygons):
    """
    Plots multiple 2D points and polygons provided as a dictionary.
    
    Parameters:
    named_points (dict): A dictionary where keys are point names (e.g. 'Point_E')
                         and values are coordinate lists [x, y].
    """
    plt.figure(figsize=(10, 3))
    
    # Plot named points
    for name, (x, y) in named_points.items():
        point = name.strip("Point_")
        plt.plot(x, y, 'o')
        plt.text(x + 0.05, y + 0.05, point, fontsize=9)
    
    # Loop over each polygon and plot it
    for polygon in polygons:
        # Create the named point group for each polygon
        polygon_dict = create_named_point_group(polygon["name"], *polygon["points"])

        # Plot the filled polygon
        plot_filled_polygon(polygon_dict)
    
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.title('2D visualisation of coordinates and polygons')
    plt.grid(True)
    
    # Show the plot
    plt.show()
