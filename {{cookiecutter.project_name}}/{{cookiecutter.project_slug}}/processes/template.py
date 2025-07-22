from process_bigraph import ProcessTypes, Process, Composite, default
from process_bigraph.emitter import emitter_from_wires, gather_emitter_results


class ProcessTemplate(Process):
    '''
    '''

    # The config_schema is a description of the information required
    # to construct an instance of this process. 
    config_schema = {
        'rate': 'float'}


    def initialize(self, config):
        '''
        When this process is created, 
        '''

        pass


    def inputs(self):
        return {
            'mass': 'float'}


    def outputs(self):
        return {
            'mass': 'float'}


    def update(self, state, interval):
        delta = state['mass'] * interval * self.config['rate']
        return {
            'mass': delta}


def run_process(core, config):
    state = {
        'mass': 1.0,
        'process': {
            '_type': 'process',
            'address': 'local:!{{cookiecutter.project_slug}}.processes.ProcessTemplate',
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

    results = gather_emitter_results(composite)

    assert results[-1]['time'] == duration
    assert len(results) == 101 # ?

    print(results) # !


if __name__ == '__main__':
    core = ProcessTypes()
    core.register_process(
        'template',
        ProcessTemplate)

    config = {
        'rate': 0.1}

    run_process(core, config)
