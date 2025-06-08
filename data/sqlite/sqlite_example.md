# Layout

The SQL data is laid out into three tables: Results, Meets, and Lifters.
Example rows of the tables in the database have been displayed below in their DTO forms.

## The Results Table

Head of results table:

0.	Result(result_id=1, lifter_id=1, meet_id=1, event='B', equipment='Raw', age=28.5, division='Open', bodyweight_kg=67.30000305175781, weight_class_kg=None, squat1_kg=None, squat2_kg=None, squat3_kg=None, squat4_kg=None, best3_squat_kg=None, bench1_kg=-40.0, bench2_kg=-45.0, bench3_kg=-45.0, bench4_kg=None, best3_bench_kg=None, deadlift1_kg=None, deadlift2_kg=None, deadlift3_kg=None, deadlift4_kg=None, best3_deadlift_kg=None, total_kg=None, place='DQ', dots=None, wilks=None, tested=None)
1.	Result(result_id=2, lifter_id=2, meet_id=1, event='B', equipment='Raw', age=43.5, division='Open', bodyweight_kg=73.19999694824219, weight_class_kg=None, squat1_kg=None, squat2_kg=None, squat3_kg=None, squat4_kg=None, best3_squat_kg=None, bench1_kg=80.0, bench2_kg=85.0, bench3_kg=90.0, bench4_kg=None, best3_bench_kg=90.0, deadlift1_kg=None, deadlift2_kg=None, deadlift3_kg=None, deadlift4_kg=None, best3_deadlift_kg=None, total_kg=90.0, place='1', dots=88.80000305175781, wilks=86.88999938964844, tested=None)
2.	Result(result_id=3, lifter_id=3, meet_id=1, event='B', equipment='Raw', age=26.5, division='Open', bodyweight_kg=60.599998474121094, weight_class_kg=None, squat1_kg=None, squat2_kg=None, squat3_kg=None, squat4_kg=None, best3_squat_kg=None, bench1_kg=40.0, bench2_kg=42.5, bench3_kg=45.0, bench4_kg=None, best3_bench_kg=45.0, deadlift1_kg=None, deadlift2_kg=None, deadlift3_kg=None, deadlift4_kg=None, best3_deadlift_kg=None, total_kg=45.0, place='2', dots=49.56999969482422, wilks=49.790000915527344, tested=None)
3.	Result(result_id=4, lifter_id=4, meet_id=1, event='B', equipment='Raw', age=19.5, division='Juniors 17-21', bodyweight_kg=50.29999923706055, weight_class_kg=None, squat1_kg=None, squat2_kg=None, squat3_kg=None, squat4_kg=None, best3_squat_kg=None, bench1_kg=32.5, bench2_kg=35.0, bench3_kg=-37.5, bench4_kg=None, best3_bench_kg=35.0, deadlift1_kg=None, deadlift2_kg=None, deadlift3_kg=None, deadlift4_kg=None, best3_deadlift_kg=None, total_kg=35.0, place='2', dots=43.66999816894531, wilks=44.7599983215332, tested=None)
4.	Result(result_id=5, lifter_id=5, meet_id=1, event='B', equipment='Raw', age=19.5, division='Juniors 17-21', bodyweight_kg=63.70000076293945, weight_class_kg=None, squat1_kg=None, squat2_kg=None, squat3_kg=None, squat4_kg=None, best3_squat_kg=None, bench1_kg=40.0, bench2_kg=42.5, bench3_kg=-45.0, bench4_kg=None, best3_bench_kg=42.5, deadlift1_kg=None, deadlift2_kg=None, deadlift3_kg=None, deadlift4_kg=None, best3_deadlift_kg=None, total_kg=42.5, place='1', dots=45.400001525878906, wilks=45.2599983215332, tested=None)

## The Meets Table

Head of meets table:

0.	Meet(meet_id=1, federation='GSF-Belarus', meet_country='Belarus', meet_state=None, meet_name='Bison Power Cup', sanctioned='Yes', meet_type='Unknown')
1.	Meet(meet_id=2, federation='WPFG', meet_country='Canada', meet_state='QC', meet_name='World Police and Fire Games', sanctioned='Yes', meet_type='Unknown')
2.	Meet(meet_id=3, federation='WPC-Latvia', meet_country='Latvia', meet_state=None, meet_name='Latvian Championships', sanctioned='Yes', meet_type='Unknown')
3.	Meet(meet_id=4, federation='WPC-Latvia', meet_country='Latvia', meet_state=None, meet_name='MonsterGym Cup', sanctioned='Yes', meet_type='Unknown')
4.	Meet(meet_id=5, federation='WPC-Latvia', meet_country='Latvia', meet_state=None, meet_name='Monstergym atklātais čempionāts', sanctioned='Yes', meet_type='Unknown')

## The Lifters Table

Head of lifters table:

0.	Lifter(lifter_id=1, name='E.S. Denisenko', sex='F', country=None, state=None)
1.	Lifter(lifter_id=2, name='I.S. Lebetskaya', sex='F', country=None, state=None)
2.	Lifter(lifter_id=3, name='K. Yakimovich', sex='F', country=None, state=None)
3.	Lifter(lifter_id=4, name='A.G. Golneva', sex='F', country=None, state=None)
4.	Lifter(lifter_id=5, name='E.V. Marunevskaya', sex='F', country=None, state=None)
