import matplotlib.pyplot as plt
from datetime import datetime

def plot_cg_envelope(*pairs):
    # CG envelope data for normal category (example values)
    normal_envelope = {
        "weight": [680, 1157, 1157, 885, 680],  # in kg
        "moment": [820, 1385, 1200, 780, 605]  # in kg-mm
    }

    # CG envelope data for utility category (example values)
    utility_envelope = {
        "weight": [680, 997, 997, 885, 680],  # in kg
        "moment": [705, 1020, 955, 780, 605]  # in kg-mm
    }

    # Calculate centroid of the normal category envelope
    normal_centroid_moment = sum(normal_envelope["moment"]) / len(normal_envelope["moment"])
    normal_centroid_weight = sum(normal_envelope["weight"]) / len(normal_envelope["weight"])

    # Calculate centroid of the utility category envelope
    utility_centroid_moment = sum(utility_envelope["moment"]) / len(utility_envelope["moment"])
    utility_centroid_weight = sum(utility_envelope["weight"]) / len(utility_envelope["weight"])

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6, 10))

    # Plot normal category envelope
    ax.plot(normal_envelope["moment"], normal_envelope["weight"], color="black")
    # Add text for normal category
    ax.text(normal_centroid_moment, normal_centroid_weight, "Normal Category", fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=1))

    # Plot utility category envelope
    ax.plot(utility_envelope["moment"], utility_envelope["weight"], color="blue", linestyle="--")
    # Add text for utility category
    ax.text(utility_centroid_moment - 70, utility_centroid_weight - 15, "Utility Category", fontsize=12, bbox=dict(facecolor='white', edgecolor='blue', alpha=1))

    # Plot each pair of loaded airplane moment and weight
    for i, (loaded_airplane_moment, loaded_airplane_weight) in enumerate(pairs):
        ax.scatter(loaded_airplane_moment, loaded_airplane_weight, color="red", label=f"Scenario {i+1}")
        ax.text(loaded_airplane_moment - 75, loaded_airplane_weight - 11, f'({loaded_airplane_moment:.0f}:{loaded_airplane_weight:.0f})', fontsize=10, color='red')

    # Labels and title
    ax.set_xlabel("Loaded Airplane Moment (kg-mm)")
    ax.set_ylabel("Loaded Airplane Weight (kg)")
    ax.set_title("C172S CENTER OF GRAVITY MOMENT ENVELOPE")

    # Increase grid granularity
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Show minor ticks for more granularity
    ax.minorticks_on()

    # Save the plot as a PDF with timestamp
    plt.savefig(f'Outputs/cg moment envelope {datetime.now().strftime("%d-%b-%y %H%M")}.pdf')

    # Turn on interactive mode
    plt.ion()
    # Display the plot
    plt.show()

    # Pause to allow the plot to be displayed while the code continues
    plt.pause(0.1)

    # Display the plot
    plt.show()


#dummy vals
#plot_cg_envelope((1172, 1087),(1124,1048))