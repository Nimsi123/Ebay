import timeit

def timer(function):
	total_time = 0
	total_calls = 0
	def new_function(*args, **kwargs):
		nonlocal total_time, total_calls
		start_time = timeit.default_timer()
		rv = function(*args, **kwargs)
		elapsed = timeit.default_timer() - start_time

		total_time += elapsed
		total_calls += 1

		print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=total_time/total_calls))
		return rv
	return new_function