from infra.modules.sensors.mpr121 import electrodes


class SimulatorElectrodes(electrodes.ElectrodesGrid):

    def __init__(self, grid_sizes, pixel_sizes, paws, led_map, mid_pixel):
        electrodes.ElectrodesGrid.__init__(self, grid_sizes, pixel_sizes)
        self.paws = paws
        for i in self.electrodes:
            i.mid_point = ([led_map[p] - mid_pixel for p in i.mid_pixel])

    def update(self):
        self.paws.update_window_mask()
        for i in self.electrodes:
            i._set_touched(self.paws.window_mask.get_at(i.mid_point))
