import matplotlib.pyplot as plt
from gbcall import defineExpose, types


@defineExpose(
    input=[types.Number, types.Number],
    output=[types.Plot]
)
def plot(apple, blueberry):

    fig, ax = plt.subplots()

    fruits = ['apple', 'blueberry', 'cherry', 'orange']
    counts = [apple, blueberry, 30, 55]
    bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

    ax.bar(fruits, counts, color=bar_colors)

    ax.set_ylabel('fruit supply')
    ax.set_title('Fruit supply by kind and color')

    return fig
