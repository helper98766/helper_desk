class Updatable:
    def override(self, **kwargs):
        """
        Creates a new instance of the current class with updated attributes.

        Args:
            **kwargs: Key-value pairs to override the current instance's attributes.

        Returns:
            A new instance of the class with the updated attributes.
        """
        # Create a copy of the current instance's attributes
        new_kwargs = self.__dict__.copy()
        # Update with the new attributes provided in kwargs
        new_kwargs.update(**kwargs)
        # Return a new instance of the same class with updated attributes
        return self.__class__(**new_kwargs)
