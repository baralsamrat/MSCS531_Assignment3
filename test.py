def configure_caches(size, assoc):
    # Configure L1 caches
    system.cpu.icache = Cache(size=size, assoc=assoc)
    system.cpu.dcache = Cache(size=size, assoc=assoc)

    # Optionally add L2 cache
    system.cpu.l2cache = Cache(size='256kB', assoc=8)  # Keep L2 constant for this example

    # Connect caches
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)
    system.cpu.icache.connectBus(system.membus)
    system.cpu.dcache.connectBus(system.membus)
    system.cpu.l2cache.connectCPU(system.cpu)
    system.cpu.l2cache.connectBus(system.membus)

# Example call: change these parameters for different experiments
configure_caches('32kB', 2)  # Change to different sizes and associativity


# Add a prefetcher to the L1 data cache
system.cpu.dcache.prefetcher = StridePrefetcher()  # You can choose other prefetcher types too


# Configure the MMU
system.mmu = SystemXBar()

# Create an MMU and connect it to the CPU and memory bus
system.cpu.mmu = simple.MMU()
system.cpu.mmu.connectBus(system.membus)

# Use a page table
system.cpu.mmu.page_table = PageTable()
system.cpu.mmu.enable_virtual_memory = True  # Enable virtual memory

# Set a workload that utilizes virtual memory
process.cmd = ['your_virtual_memory_application_here']  # Ensure your application uses memory management


from m5.objects import *
from m5.util import *

def configure_caches(size, assoc):
    # Configure L1 caches
    system.cpu.icache = Cache(size=size, assoc=assoc)
    system.cpu.dcache = Cache(size=size, assoc=assoc)

    # Optionally add L2 cache
    system.cpu.l2cache = Cache(size='256kB', assoc=8)  # Keep L2 constant for this example

    # Connect caches
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)
    system.cpu.icache.connectBus(system.membus)
    system.cpu.dcache.connectBus(system.membus)
    system.cpu.l2cache.connectCPU(system.cpu)
    system.cpu.l2cache.connectBus(system.membus)

def run_simulation():
    # Set up the system
    system = System()
    system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
    system.cpu = TimingSimpleCPU()
    system.mem_ranges = [AddrRange('512MB')]
    system.membus = SystemXBar()
    system.mem_ctrl = DDR3_1600_8x8()
    system.mem_ctrl.range = system.mem_ranges[0]
    system.membus.connectBus(0, system.mem_ctrl.port)

    # Set the workload
    process = Process(pid=1234)
    process.cmd = ['your_application_here']  # Replace with your binary
    system.cpu.workload = process
    system.cpu.createThreads()

    # Set up the root of the simulation
    root = Root(full_system=False, system=system)
    m5.instantiate()

    # Run the simulation
    print("Beginning simulation!")
    exit_event = m5.simulate()
    print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))

# Experiment with different cache sizes and associativity
for cache_size in ['16kB', '32kB', '64kB']:
    for cache_assoc in [2, 4, 8]:
        print(f"Running experiment with cache size: {cache_size}, associativity: {cache_assoc}")
        configure_caches(cache_size, cache_assoc)
        run_simulation()

# Implement prefetching experiments
def configure_prefetching():
    # Example: Adding a stride prefetcher to the data cache
    system.cpu.dcache.prefetcher = StridePrefetcher()

# Example loop for prefetching experiments
for prefetcher in [None, StridePrefetcher(), SpatialPrefetcher()]:
    print(f"Running experiment with prefetcher: {prefetcher}")
    configure_caches('32kB', 4)  # Use a fixed cache size/assoc for simplicity
    if prefetcher:
        system.cpu.dcache.prefetcher = prefetcher
    run_simulation()

# Implement virtual memory experiments
def configure_virtual_memory():
    # Configure the MMU
    system.mmu = SystemXBar()
    system.cpu.mmu = simple.MMU()
    system.cpu.mmu.connectBus(system.membus)

    # Set a workload that utilizes virtual memory
    process.cmd = ['your_virtual_memory_application_here']  # Ensure your application uses memory management

# Example loop for virtual memory experiments
print("Running virtual memory experiment")
configure_virtual_memory()
run_simulation()
