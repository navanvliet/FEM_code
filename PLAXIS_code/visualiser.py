import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

diameters = np.round(np.arange(0.1, 0.4, 0.025), 3) # [m]

# include diameter name in file

def plot_pile_data(diameters):
    
    N = "N"
    Q = "Q"
    M = "M"

    # Create the subplots
    fig, axes = plt.subplots(3, 3, figsize=(10, 15), sharex=True)

    for select in range(len(diameters)):
        # Load the CSV file
        csv_filename = f"pile_D{diameters[select]}.csv" # Replace with your actual file name
        data = pd.read_csv(csv_filename)

        # Filter data based on pile_number
        pile_1_data = data[data["pile_number"] == 1]
        pile_2_data = data[data["pile_number"] == 2]
        pile_3_data = data[data["pile_number"] == 3]

        for j in range(3):
            # Get the column name for the current subplot
            column_name = [N, Q, M][j]

            # Plot data for pile 1
            axes[0][j].plot(pile_1_data[column_name], pile_1_data["y"], label=f"D = {diameters[select]:.3f} m")
            axes[0][j].set_title(f"Pile 1: {column_name} over Depth")
            axes[0][j].set_xlabel(f"{column_name} [kNm]")
            axes[0][j].set_ylabel("Depth [m]")
            # axes[0][j].set_xlim(-80, 0)  # Set x-axis limits
            axes[0][j].legend(fontsize='xx-small')
            axes[0][j].grid()

            # Plot data for pile 2
            axes[1][j].plot(pile_2_data[column_name], pile_2_data["y"], label=f"D = {diameters[select]:.3f} m")
            axes[1][j].set_title(f"Pile 2: {column_name} over Depth")
            axes[1][j].set_xlabel(f"{column_name} [kNm]")
            axes[1][j].set_ylabel("Depth [m]")
            # axes[1][j].set_xlim(-20, 20)  # Set x-axis limits
            axes[1][j].legend(fontsize='xx-small')
            axes[1][j].grid()

            # Plot data for pile 3
            axes[2][j].plot(pile_3_data[column_name], pile_3_data["y"], label=f"D = {diameters[select]:.3f} m")
            axes[2][j].set_title(f"Pile 3: {column_name} over Depth")
            axes[2][j].set_xlabel(f"{column_name} [kNm]")
            # axes[2][j].set_xlim(-40, 20)  # Set x-axis limits
            axes[2][j].set_ylabel("Depth [m]")
            axes[2][j].legend(fontsize='xx-small')
            axes[2][j].grid()

    # Adjust layout
    plt.tight_layout()
    plt.show()

plot_pile_data(diameters)
