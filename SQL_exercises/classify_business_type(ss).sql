-- Classify Business Type
-- Classify each business as either a restaurant, cafe, school, or other. A restaurant should have the word 'restaurant' in the business name. 
-- For cafes, either 'cafe', 'caf?', or 'coffee' can be in the business name. 'School' should be in the business name for schools. 
-- All other businesses should be classified as 'other'. Output the business name and the calculated classification
-- https://platform.stratascratch.com/coding/9726-classify-business-type?code_type=1

# sf_restaurant_health_violations
# business_id: int
# business_name: varchar
# business_address: varchar
# business_city: varchar
# business_state: varchar
# business_postal_code: float
# business_latitude: float
# business_longitude: float
# business_location: varchar
# business_phone_number: float
# inspection_id: varchar
# inspection_date: datetime
# inspection_score: float
# inspection_type: varchar
# violation_id: varchar


select distinct business_name, case when business_name ilike '%cafe%' or 
                                business_name ilike '%coffee%' or 
                                business_name ilike '%café%'   then 'cafe'
                           when business_name ilike '%restaurant%' then 'restaurant' 
                           when business_name ilike '%school%' then 'school'
                           else 'other' end as business_type 
from sf_restaurant_health_violations

