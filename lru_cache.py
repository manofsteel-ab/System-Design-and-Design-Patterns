
from abc import ABC,abstractmethod 


class CacheLine:
	def __init__(self, key=0, value=0):
		self.key = key
		self.value = value
		self.prev = None
		self.next = None

	def set_next(self, next_cachline):
		self.next = next_cachline

	def set_prev(self, prev_cachline):
		self.prev = prev_cachline

	def get_next(self):
		return self.next

	def get_prev(self):
		return self.prev

	def delete(self):
		self.set_next(None)
		self.set_prev(None)


class DefaultCachInterface(ABC):
	# interface to create cache using cachline datastructure

	@abstractmethod
	def put(self, key: int, value: int):
		pass

	@abstractmethod
	def get(self, key: int):
		pass


class LRUCache(DefaultCachInterface):

	def __init__(self, capacity: int):
		self.cache = {}
		self.capacity = capacity
		self.size = 0
		self.head = CacheLine()
		self.tail = CacheLine()
		self.head.set_next(self.tail)
		self.tail.set_prev(self.head)


	def get(self, key: int):
		if key in self.cache:
			cache_line = self.cache.get(key)
			new_cachline = CacheLine(cache_line.key, cache_line.value)
			self._remove(cache_line)
			self._insert_at_front(new_cachline)

		return -1


	def put(self, key: int, value:int):
		new_cachline = CacheLine(key, value)
		if key in self.cache:
			# if key already present in cache then move it at front
			cache_line = self.chache.get(key)
			self._remove(cache_line)
			self._insert_at_front(new_cachline)


		if self.size+1 > self.capacity:
			# if cache is full then delete last node 
			tail_prev = self.tail_prev
			self._remove(self.tail)
			self.tail = tail_prev

		self._insert_at_front(new_cachline)




	def _remove(self, node):
		# remove node from 
		prev = node.get_prev()
		nxt = node.get_next()
		if prev:
			prev.set_next(nxt)
		if nxt:
			nxt.set_prev(prev)
		node.delete()
		self.size = self.size - 1


	def _insert_at_front(self, node):
		# insert at front of doubly linked list
		node.set_prev(None)
		node.set_next(self.head)
		self.head = node
		self.size = self.size + 1


class CacheType:
	LRU = 'lru'


class CacheFactorInterface(ABC):

	@abstractmethod
	def get_cache(self, cache_type, capacity):
		pass


class CacheFactory(CacheFactorInterface):

	def get_cache(self, cache_type, capacity):
		if cache_type == CacheType.LRU:
			return LRUCache(capacity)
		else:
			raise Exception("Unsupported chache type")






