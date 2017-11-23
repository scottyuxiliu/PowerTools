import matplotlib.pyplot as plt


class Plot:
    """plotting functions"""

    def line(self, x, y, title=None, subplots=False):
        plt.figure()
        plt.plot(x, y, linewidth=2.0)
        plt.title(title)
        return 0
    def stackedline(self, x, y_df, title=None, subplots=False):
        plt.figure()
        for y_col in y_df:
            plt.plot(x, y_df[y_col], linewidth=1.0, label=y_col)
        plt.legend(loc='upper right')
        plt.title(title)
        return 0