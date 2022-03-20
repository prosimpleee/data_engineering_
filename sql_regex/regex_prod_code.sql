

insert into regex_2 values
('ProductCode :11111'),
('ProductCode :12345'),
('ProductCode :9421412'),
('ProductCode :14245154'),
('ProductCode :87756731'),
('ProductCode :00041242'),
('ProductCode :441241'),
('ProductCode :4109090022'),
('ProductCode :45561'),
('ProductCode :4524967761'),
('ProductCode :6675478451');

-- Equal: '\d+', ':(\d+)'
select substring(prod_code from '(\d+)') as prod_code
from regex_2 r 