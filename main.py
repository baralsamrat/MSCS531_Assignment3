from m5.objects import *
from m5.util import *

# Create the system
system = System()

# Set up the CPU
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())

# Configure the CPU
system.cpu = TimingSimpleCPU()

# Set up memory
system.mem_ranges = [AddrRange('512MB')]

# Create the memory bus
system.membus = SystemXBar()

# Configure the main memory
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.membus.connectBus(0, system.mem_ctrl.port)

# Configure L1 caches
system.cpu.icache = Cache(size='32kB', assoc=2)
system.cpu.dcache = Cache(size='32kB', assoc=2)

# Optionally add L2 cache
system.cpu.l2cache = Cache(size='256kB', assoc=8)

# Connect caches
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)
if hasattr(system.cpu, 'l2cache'):
    system.cpu.l2cache.connectCPU(system.cpu)
    system.cpu.l2cache.connectBus(system.membus)

# Set the workload
process = Process(pid=1234)
process.cmd = ['your_application_here']  # Replace with the path to your binary
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root of the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

# Run the simulation
print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))