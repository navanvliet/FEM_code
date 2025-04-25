from plxscripting.easy import *
import pandas as pd

# Create soil
def create_soil(s_i, g_i):
    df = pd.read_csv("soillayers.csv", skiprows=[0], encoding='latin1')

    # Iterate over the rows of the dataframe and create materials
    for _, row in df.iterrows():
        # Extract the necessary parameters from the row
        params = [
            ("SoilModel", "HS small"),
            ("Identification", row['Dutchname']),
            ("E50ref", row['E50ref']),
            ("phi", row['phi']),
            ("cref", row['cref']),
            ("psi", row['psi']),
            ("gammaunsat", row['gammadry']),
            ("gammasat", row['gammasat']),
            ("Eoedref", row['Eoedref']),
            ("Eurref", row['Eurref']),
            ("gamma07", row['gamma07']),
            ("G0ref", row['G0ref']),
            ("powerm", row['m'])
        ]
        
        # Create the soil material using the g_i.soilmat function
        material = g_i.soilmat(*params)

    # Set Allerod material with different properties, otherwise the program throws error
    g_i.Allerod.EOedRef = 7567

    # Initialize soil contour
    xmin = -15
    xmax = 15
    ymin = -20
    ymax = 0.580
    g_i.SoilContour.initializerectangular(xmin, ymin, xmax, ymax)

    # Set borehole
    g_i.borehole(0)
    g_i.Borehole_1.Head = -0.4 # [m]

    # Define the number of soil layers
    n_soillayers = 7
    for n in range(n_soillayers):
        g_i.soillayer(1)

    # Adjust thickness of the soil layers
    g_i.Soillayer_1.Zones[0].Top = -2.4
    g_i.Soillayer_1.Zones[0].Bottom = -5
    g_i.Soillayer_2.Zones[0].Bottom = -12
    g_i.Soillayer_3.Zones[0].Bottom = -12.5
    g_i.Soillayer_4.Zones[0].Bottom = -13
    g_i.Soillayer_5.Zones[0].Bottom = -15
    g_i.Soillayer_6.Zones[0].Bottom = -17
    g_i.Soillayer_7.Zones[0].Bottom = ymin

    # Apply soil layer materials
    g_i.Soil_1.Material = [m for m in g_i.Materials if m.Name == 'Hollandveen'][0]
    g_i.Soil_2.Material = [m for m in g_i.Materials if m.Name == 'Wadzand'][0]
    g_i.Soil_3.Material = [m for m in g_i.Materials if m.Name == 'Hydrobiaklei'][0]
    g_i.Soil_4.Material = [m for m in g_i.Materials if m.Name == 'Basisveen'][0]
    g_i.Soil_5.Material = [m for m in g_i.Materials if m.Name == 'EersteZandlaag'][0]
    g_i.Soil_6.Material = [m for m in g_i.Materials if m.Name == 'Allerod'][0]
    g_i.Soil_7.Material = [m for m in g_i.Materials if m.Name == 'TweedeZandlaag'][0]

    # Soil_I
    y_kesp = -1.104 # [m] height of the kesp
    y_GL = 0.58 # [m] ground level
    y_A = -2.4 # [m]
    x_A = (y_A - y_kesp)*3
    y_B = -2 # [m]
    x_B = (y_B - y_kesp)*3
    x_C = xmax # [m]
    y_C = y_B # [m]
    x_D = xmax # [m]
    y_D = y_A # [m]
    Point_A = [x_A, y_A]
    Point_B = [x_B, y_B]
    Point_C = [x_D, y_C]
    Point_D = [x_C, y_D]

    # Soil_II
    x_E, y_E = 0, y_kesp # [m], [m]
    x_F, y_F = 2.4, y_kesp # [m], [m]
    y_G = y_GL - 0.5 # [m]
    x_G = x_F + (y_G - y_F)*3 # [m]
    x_H, y_H = xmax, y_G # [m], [m]
    Point_E = [x_E, y_E]
    Point_F = [x_F, y_F]
    Point_G = [x_G, y_G]
    Point_H = [x_H, y_H]

    # Soil_III
    y_I = y_G # [m]
    x_I = (y_I - y_E)*3 # [m]
    x_H, y_H = xmax, y_G # [m], [m]
    Point_I = [x_I, y_I]

    # Soil_IV
    x_J, y_J = 0.65, y_H # [m], [m]
    x_K, y_K = x_J, y_kesp # [m], [m]
    Point_J = [x_J, y_J]
    Point_K = [x_K, y_K]

    # Soil_V
    x_L, y_L = x_J, y_GL # [m], [m]
    x_M, y_M = xmax, y_GL # [m], [m]
    Point_L = [x_L, y_L]
    Point_M = [x_M, y_M]

    # Wall
    x_N, y_N = x_E, y_GL # [m], [m]
    Point_N = [x_N, y_N]

    # Kesp
    x_O, y_O = -0.3, y_kesp # [m], [m]
    Point_O = [x_O, y_O]

    points = {
        "Point_A": Point_A,
        "Point_B": Point_B,
        "Point_C": Point_C,
        "Point_D": Point_D,
        "Point_E": Point_E,
        "Point_F": Point_F,
        "Point_G": Point_G,
        "Point_H": Point_H,
        "Point_I": Point_I,
        "Point_J": Point_J,
        "Point_K": Point_K,
        "Point_L": Point_L,
        "Point_M": Point_M,
        "Point_N": Point_N,
        "Point_O": Point_O}

    polygons = [
        {"name": "Soil_I", "points": [Point_A, Point_B, Point_C, Point_D]},
        {"name": "Soil_II", "points": [Point_B, Point_E, Point_F, Point_G, Point_H, Point_C]},
        {"name": "Soil_III", "points": [Point_E, Point_I, Point_G, Point_F]},
        {"name": "Soil_IV", "points": [Point_K, Point_J, Point_G, Point_F]},
        {"name": "Soil_V", "points": [Point_J, Point_L, Point_M, Point_H]},
        {"name": "Wall", "points": [Point_E, Point_N, Point_L, Point_K]}]

    g_i.polygon(Point_A, Point_B, Point_C, Point_D)
    g_i.Polygon_1.Name = 'Soil_I'
    g_i.Soil_8.Material = [m for m in g_i.Materials if m.Name == 'Hollandveen'][0]

    g_i.polygon(Point_B, Point_E, Point_F, Point_G, Point_H, Point_C)
    g_i.Polygon_1.Name = 'Soil_II'
    g_i.Soil_9.Material = [m for m in g_i.Materials if m.Name == 'GeulopvullingKlei'][0]

    g_i.polygon(Point_E, Point_I, Point_G, Point_F)
    g_i.Polygon_1.Name = 'Soil_III'
    g_i.Soil_10.Material = [m for m in g_i.Materials if m.Name == 'GeulopvullingKlei'][0]

    g_i.polygon(Point_K, Point_J, Point_G, Point_F)
    g_i.Polygon_1.Name = 'Soil_IV'
    g_i.Soil_11.Material = [m for m in g_i.Materials if m.Name == 'GeulopvullingKlei'][0]

    g_i.polygon(Point_J, Point_L, Point_M, Point_H)
    g_i.Polygon_1.Name = 'Soil_V'
    g_i.Soil_12.Material = [m for m in g_i.Materials if m.Name == 'Verharding'][0]
    