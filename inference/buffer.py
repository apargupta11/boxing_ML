from collections import deque


class RollingBuffer:

    def __init__(self, max_samples=300):

        """
        Rolling buffer for incoming IMU packets.

        Parameters
        ----------
        max_samples : int
            Maximum number of samples to keep.
        """

        self.buffer = deque(maxlen=max_samples)

    # ====================================================
    # Add Sample
    # ====================================================

    def add(self, sample):

        """
        Add one IMU sample.

        Parameters
        ----------
        sample : dict
        """

        self.buffer.append(sample)

    # ====================================================
    # Get Entire Buffer
    # ====================================================

    def get_all(self):

        """
        Returns all samples.
        """

        return list(self.buffer)

    # ====================================================
    # Get Last N Samples
    # ====================================================

    def last(self, n):

        """
        Returns the last N samples.
        """

        return list(self.buffer)[-n:]

    # ====================================================
    # Get Sample by Index
    # ====================================================

    def get(self, index):

        """
        Returns one sample.
        """

        return self.buffer[index]

    # ====================================================
    # Current Buffer Size
    # ====================================================

    def size(self):

        return len(self.buffer)

    # ====================================================
    # Check Empty
    # ====================================================

    def is_empty(self):

        return len(self.buffer) == 0

    # ====================================================
    # Clear Buffer
    # ====================================================

    def clear(self):

        self.buffer.clear()

    # ====================================================
    # Remove Oldest Sample
    # ====================================================

    def pop_left(self):

        if self.buffer:

            return self.buffer.popleft()

        return None

    # ====================================================
    # Remove Latest Sample
    # ====================================================

    def pop_right(self):

        if self.buffer:

            return self.buffer.pop()

        return None