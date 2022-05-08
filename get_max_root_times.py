import msprime

pop_sizes = [10, 100, 1_000]
sequence_lengths = [1_000, 10_000, 100_000]
recombination_rate_exps = [-7, -8, -9]
seeds = [1, 2]

with open("output.csv", "w+") as f:
    f.write("pop_size,\t sequence_length,\t recombination_rate,\t random_seed,\t dtwf_vs_hudson,\t selective_sweep,\t max_root_time\n")

    for pop_size in pop_sizes:
        for sequence_length in sequence_lengths:
            sweep_model = msprime.SweepGenicSelection(position=sequence_length/2, start_frequency=0.0001, end_frequency=0.1, s=0.25,dt=1e-2)
        
            for recombination_rate_exp in recombination_rate_exps:
                for seed in seeds:
                    ts00 = msprime.sim_ancestry(10,
                         model=["dtwf"],
                         population_size=pop_size,
                         sequence_length=sequence_length,
                         recombination_rate=10 ** recombination_rate_exp,
                         random_seed=seed,
                         )
                    f.write("%d,\t %d,\t %d,\t %d,\t %d,\t %d,\t %f\n" % (pop_size, sequence_length, recombination_rate_exp, seed, 0, 0, ts00.max_root_time))
                    ts01 = msprime.sim_ancestry(10,
                         model=[sweep_model, "dtwf"],
                         population_size=pop_size,
                         sequence_length=sequence_length,
                         recombination_rate=10 ** recombination_rate_exp,
                         random_seed=seed,
                         )
                    f.write("%d,\t %d,\t %d,\t %d,\t %d,\t %d,\t %f\n" % (pop_size, sequence_length, recombination_rate_exp, seed, 0, 1, ts01.max_root_time))
                    ts10 = msprime.sim_ancestry(10,
                         model=["hudson"],
                         population_size=pop_size,
                         sequence_length=sequence_length,
                         recombination_rate=10 ** recombination_rate_exp,
                         random_seed=seed,
                         )
                    f.write("%d,\t %d,\t %d,\t %d,\t %d,\t %d,\t %f\n" % (pop_size, sequence_length, recombination_rate_exp, seed, 1, 0, ts10.max_root_time))
                    ts11 = msprime.sim_ancestry(10,
                         model=[sweep_model, "hudson"],
                         population_size=pop_size,
                         sequence_length=sequence_length,
                         recombination_rate=10 ** recombination_rate_exp,
                         random_seed=seed,
                         )
                    f.write("%d,\t %d,\t %d,\t %d,\t %d,\t %d,\t %f\n" % (pop_size, sequence_length, recombination_rate_exp, seed, 1, 1, ts11.max_root_time))
