from process_bigraph import ProcessTypes, Process, Composite, default
from process_bigraph.emitter import emitter_from_wires, gather_emitter_results


class ProcessTemplate(Process):
    """
    A simple template process that scales a 'mass' value by a fixed rate
    at each update interval. This example illustrates how to define a custom
    Process in the process-bigraph framework.
    """

    # The config_schema is a description of the information required
    # to construct an instance of this process.
    config_schema = {
        'rate': 'float'}

    def initialize(self, config):
        """
        Initialize the process with configuration parameters.

        Parameters
        ----------
        config : dict
            Configuration dictionary containing the 'rate' parameter.
        """
        pass

    def inputs(self):
        """
        Define the input variables for the process.

        Returns
        -------
        dict
            A dictionary mapping variable names to their types.
            This process expects one input: 'mass' of type float.
        """
        return {
            'mass': 'float'}

    def outputs(self):
        """
        Define the output variables for the process.

        Returns
        -------
        dict
            A dictionary mapping variable names to their types.
            This process outputs 'mass' of type float.
        """
        return {
            'mass': 'float'}

    def update(self, state, interval):
        """
        Compute the update to the mass based on the rate and time interval.

        Parameters
        ----------
        state : dict
            Dictionary containing the current state values.
        interval : float
            Duration over which the update occurs.

        Returns
        -------
        dict
            Dictionary with the computed delta in 'mass'.
        """
        # Extract the current mass from the input port
        mass = state['mass']

        # Calculate the change in mass based on the rate and interval
        delta = self.config['rate'] * mass * interval

        # Return the change to mass as output
        return {
            'mass': delta}


def run_process(core):
    """
    Run a simple simulation using the ProcessTemplate.
    """

    config = {
        'rate': 0.1}

    state = {
        'mass': 1.0,
        'process': {
            '_type': 'process',
            'address': 'local:!{{cookiecutter.project_slug}}.processes.template.ProcessTemplate',
            'config': config,
            'inputs': {'mass': ['mass']},
            'outputs': {'mass': ['mass']},
            'interval': 1.0},

        'emitter': emitter_from_wires({
            'time': ['global_time'],
            'mass': ['mass']})}

    composite = Composite({
        'state': state}, core=core)

    duration = 10.0
    composite.run(duration)

    results = gather_emitter_results(composite)[('emitter',)]

    assert results[-1]['time'] == duration
    assert len(results) == 11  # 0 to 10 inclusive

    print(results)


if __name__ == '__main__':
    core = ProcessTypes()
    core.register_process(
        'template',
        ProcessTemplate)

    run_process(core)
