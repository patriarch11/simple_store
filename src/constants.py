from enum import Enum


DB_NAMING_CONVENTION = {
	'ix': '%(column_0_label)s_idx',
	'uq': '%(table_name)s_%(column_0_name)s_key',
	'ck': '%(table_name)s_%(constraint_name)s_check',
	'fk': '%(table_name)s_%(column_0_name)s_fkey',
	'pk': '%(table_name)s_pkey',
}

LOG_FORMAT = '{time} {level} {message}'


class Environment(str, Enum):
	LOCAL      = 'LOCAL'
	TESTING    = 'TESTING'
	STAGING    = 'STAGING'
	PRODUCTION = 'PRODUCTION'

	@property
	def is_debug(self):
		return self in (self.LOCAL, self.TESTING)

	@property
	def is_testing(self):
		return self == self.TESTING

	@property
	def is_deployed(self) -> bool:
		return self in (self.STAGING, self.PRODUCTION)

	@property
	def is_local(self) -> bool:
		return self == self.LOCAL


class OrderStatus(Enum):
	RESERVED  = 1
	COMPLETED = 2
	CANCELLED = 3


class SalesReportOrder(Enum):
	AMOUNT           = 'AMOUNT'
	DATE             = 'DATE'
	QUANTITY         = 'QUANTITY'
	PRODUCT_PRICE    = 'PRODUCT_PRICE'
	PRODUCT_DISCOUNT = 'PRODUCT_DISCOUNT'


class SortOrder(Enum):
	ASCENDING  = 'ASCENDING'
	DESCENDING = 'DESCENDING'
