from plxscripting.easy import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.path import Path
from geometry import plot_geometry
from soil import create_soil

# Initialize Input server
localhost_input = 10000
password_input = 'YQ+R8$e5xy+G26z~'
s_i, g_i = new_server('localhost', localhost_input, password=password_input)


# Initialize output server
localhost_output = 10001
password_output = 'YQ+R8$e5xy+G26z~'
s_o, g_o = new_server('localhost', localhost_output, password=password_output)

D_array = np.round(np.arange(0.1, 0.4, 0.025), 3)  # [m]
fmax_values = D_array/0.2*100  # [kN]

xmin = -15
xmax = 15
ymin = -20
ymax = 0.580
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

for select in range(len(D_array)):

    fmax_values[select] = D_array[select]/0.2*100 # [kN]

    s_i.open(r'C:\Users\nielsvanvliet\PLAXIS_models\test.p2dx')

    create_soil(s_i, g_i)

    g_i.gotostructures()

    # Create a plate material
    EA = 1.21e9 # [kN/m] = [N/mm]
    EI = 6.88e9*1e-6 # [kN/m^2/m] = 10^6 [N/mm^2/mm]
    nu = 0.35

    g_i.platemat("Identification", "Timber_Kesp",
                "MaterialType", "Elastic",
                "EA1", EA,
                "EI", EI,
                "StructNu", nu)

    # Create plate
    Kesp_Line = g_i.line(Point_O, Point_F)
    g_i.Line_1.Name = 'Kesp_Line'

    Kesp = g_i.plate(g_i.Kesp_Line)
    g_i.Plate_1.Name = 'Kesp'

    # Assign material to plate
    g_i.Kesp.Material = [m for m in g_i.Materials if m.Name == 'Timber_Kesp'][0]

    # Add positive interface
    g_i.posinterface(g_i.Kesp_Line)
    g_i.PositiveInterface_1.Name = 'Positive_IF_Kesp'

    # Add negative interface
    g_i.neginterface(g_i.Kesp_Line)
    g_i.NegativeInterface_1.Name = 'Negative_IF_Kesp'

    # Create geometry wall
    g_i.polygon(Point_E, Point_N, Point_L, Point_K)
    g_i.Polygon_1.Name = 'Wall'

    # Create wall material
    E_masonry = 8e6 # [kN/m^2]
    nu_masonry = 0.2 # [-]
    gammaunsat_masonry = 19.5 # [kN/m^3]

    g_i.soilmat("Identification", "Masonry",
                "SoilModel", "Linear Elastic",
                "DrainageType", "Non-porous",
                "gammaunsat", gammaunsat_masonry,
                "Eref", E_masonry,
                "nu", nu_masonry)

    # Assign wall material
    g_i.Soil_13.Material = [m for m in g_i.Materials if m.Name == 'Masonry'][0]

    # Create geometry piles
    n_piles = 3
    pile_spacing = 1.1 #[m]

    # geometry pile 1
    pile_1_x_bot = 0.1375 
    pile_1_y_bot = -13.29
    pile_1_x_top = pile_1_x_bot
    pile_1_y_top = -1.104

    Point_1_Pile_1 = [pile_1_x_bot, pile_1_y_bot]
    Point_2_Pile_1 = [pile_1_x_top, pile_1_y_top]

    # geometry pile 2
    pile_2_x_bot = 0.1375 + pile_spacing
    pile_2_y_bot = -13.29
    pile_2_x_top = pile_2_x_bot
    pile_2_y_top = -1.104

    Point_1_Pile_2 = [pile_2_x_bot, pile_2_y_bot]
    Point_2_Pile_2 = [pile_2_x_top, pile_2_y_top]

    # geometry pile 3
    pile_3_x_bot = 0.1375 + 2*pile_spacing
    pile_3_y_bot = -13.29
    pile_3_x_top = pile_3_x_bot
    pile_3_y_top = -1.104

    Point_1_Pile_3 = [pile_3_x_bot, pile_3_y_bot]
    Point_2_Pile_3 = [pile_3_x_top, pile_3_y_top]

    # Create timber material
    E_timber = 11e6 # [kN/m^2]
    nu_timber = 0.35 # [-]

    # Create piles
    Pile_1 = g_i.embeddedbeam(Point_1_Pile_1, Point_2_Pile_1)
    Pile_2 = g_i.embeddedbeam(Point_1_Pile_2, Point_2_Pile_2)
    Pile_3 = g_i.embeddedbeam(Point_1_Pile_3, Point_2_Pile_3)

    # Rename embedded beams
    g_i.EmbeddedBeam_1.Name = "Pile_1"
    g_i.EmbeddedBeam_2.Name = "Pile_2"
    g_i.EmbeddedBeam_3.Name = "Pile_3"

    # Rename lines piles
    g_i.Line_1.Name = 'Pile_1_Line'
    g_i.Line_2.Name = 'Pile_2_Line'
    g_i.Line_3.Name = 'Pile_3_Line'
    
    E_timber = 11e6 # [kN/m^2] Stiffness
    D = D_array[select] # [m] Diameter
    L_spacing = 1 # [m]
    Gamma_Timber = 4.2 # [kN/m^3] Density
    F_max = fmax_values[select] # [kN] Base resistance


    # Create Timber_Pile material
    g_i.embeddedbeammat(("Identification", "Timber_Pile"),
                        ("MaterialType", "Elastic"),
                        ("Gamma", Gamma_Timber),
                        ("Lspacing", L_spacing),
                        ("Diameter", D),
                        ("E", E_timber),
                        ("Fmax",F_max))

    # Assign Timber_Pile material to Embedded beams
    g_i.Pile_1.Material = [m for m in g_i.Materials if m.Name == 'Timber_Pile'][0]
    g_i.Pile_2.Material = [m for m in g_i.Materials if m.Name == 'Timber_Pile'][0]
    g_i.Pile_3.Material = [m for m in g_i.Materials if m.Name == 'Timber_Pile'][0]

    g_i.gotoflow()

    WL_normal = g_i.waterlevel((xmin, -0.4), (xmax, -0.4)) # [m]
    g_i.UserWaterLevel_1.Name = "WL_normal"

    WL_excavation = g_i.waterlevel((xmin, y_kesp-0.5), (xmax, y_kesp-0.5)) # [m]
    g_i.UserWaterLevel_1.Name = "WL_excavation"

    # Create the top TAK load of 10 kN/m
    g_i.gotostructures()
    line_TAK = g_i.line((x_L, y_L), (xmax, y_L))[-1]
    TAK_load = g_i.lineload(line_TAK)
    g_i.LineLoad_1.Name = "TAK_load"
    g_i.TAK_load.qy_start = -10 # [kN/m/m]

    # Go to Staged Construction
    g_i.gotostages()

    # Set initial phase idenitification
    Phase_0 = g_i.Phases[0]
    n_phases = 10
    phases = [Phase_0]

    # Create other phases in a loop
    for i in range(1, n_phases + 1):
        new_phase = g_i.phase(phases[i - 1])
        phases.append(new_phase)

    # Display all phases
    phases_id = g_i.Phases.Identification.value

    soils_phase0 = [g_i.Soil_I, g_i.Soil_II, g_i.Soil_III]

    for soil in soils_phase0:
        soil.activate(phases[0])
        
    phase = phases[1]
    phase.Deform.ResetDisplacements = True
    phase.Deform.CalculationType = "Drained"

    phase = phases[2]
    phase.Deform.ResetDisplacements = True
    phase.Deform.CalculationType = "Drained"

    g_i.setglobalwaterlevel(g_i.WL_excavation, g_i.Phase_2)

    phase = phases[3]
    phase.Deform.ResetDisplacements = True
    phase.Deform.CalculationType = "Drained"

    for phase in phases[3:]:
        g_i.Soil_III.deactivate(phase)
        
    phase = phases[4]
    phase.Deform.ResetDisplacements = True
    phase.Deform.CalculationType = "Drained"

    piles = [g_i.Pile_1, g_i.Pile_2, g_i.Pile_3]

    for pile in piles:
        for phase in phases[4:]:
            pile.activate(phase)

    phase = phases[5]
    phase.Deform.ResetDisplacements = False
    phase.Deform.CalculationType = "Drained"

    elements = [g_i.Wall, g_i.Kesp, g_i.Negative_IF_Kesp, g_i.Positive_IF_Kesp]

    for element in elements:
        for phase in phases[5:]:
            element.activate(phase)
            
    phase = phases[6]
    phase.Deform.ResetDisplacements = False
    phase.Deform.CalculationType = "Drained"

    for phase in phases[6:]:
        g_i.Soil_IV.activate(phase)
        g_i.Soil_V.activate(phase)
        
    phase = phases[7]
    phase.Deform.ResetDisplacements = False
    phase.Deform.CalculationType = "Drained"
    g_i.setglobalwaterlevel(g_i.WL_normal, g_i.Phase_7)

    phase = phases[8]
    phase.Deform.ResetDisplacements = False
    phase.Deform.CalculationType = "Drained"

    phase = phases[9]
    phase.Deform.ResetDisplacements = False
    phase.Deform.CalculationType = "Drained"

    g_i.TAK_load.activate(phase)

    g_i.gotomesh()
    g_i.mesh()

    g_i.gotostages()

    for i in range(len(phases)):
        g_i.calculate(phases[i])
        
    # Select the final phase for the forces
    phase = phases[-1]
    g_i.view(phase)

    # print(dir(g_o.ResultTypes.EmbeddedBeam)) # This helps to find the right output
    # To create an np.array for each of these results and store them in a CSV file with the respective variable names (x, y, Ux, Uy, N, Q, M) as column headers, here's the script:
    # Assuming the values are obtained from getresults and are lists or arrays
    x = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.X, "node"))
    y = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.Y, "node"))
    Ux = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.Ux, "node"))
    Uy = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.Uy, "node"))
    N = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.Nx2D, "node"))
    Q = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.Q2D, "node"))
    M = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.M2D, "node"))
    PUx = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.PUx, "node"))
    PUy = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.PUy, "node"))
    PUtot = np.array(g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.PUtot, "node"))

    # Use the geometry of the piles to split the results for the different piles by creating an index array
    def split_pile_results(n_piles=n_piles, pile_spacing=pile_spacing, pile_1_x_top=pile_1_x_top):
        x = g_o.getresults(phase, g_o.ResultTypes.EmbeddedBeam.X, "node")
        pile_number = np.zeros(len(x))

        x_pile = np.zeros(n_piles)
        for i in range(len(x_pile)):
            x_pile[i] = pile_1_x_top + pile_spacing * i

        for i in range(len(x)):
            for j in range(n_piles):
                if np.isclose(x[i], x_pile[j], rtol=1e-05, atol=1e-08):
                    pile_number[i] = int(j+1)

        return pile_number

    pile_number = split_pile_results()

    # include diameter name in file
    data = {
        "x": x,
        "y": y,
        "Ux": Ux,
        "Uy": Uy,
        "N": N,
        "Q": Q,
        "M": M,
        "PUx": PUx,
        "PUy": PUy,	
        "PUtot": PUtot,
        "pile_number": pile_number
    }
    piledf = pd.DataFrame(data)

    # Save to CSV
    csv_filename = f"pile_D{D_array[select]}.csv"
    piledf.to_csv(csv_filename, index=False)

    print(f"Data has been saved to {csv_filename}.")