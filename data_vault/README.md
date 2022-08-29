# Data Vault

I separated the mutable part from the immutable part. This can be seen in the example of a customer or store table. The gender can change, and because of this, I moved this attribute to the mutable part.

## How did I select the hubs?

- Hubs - noun/entity. Examples might be: products, customer, or currency. Hubs are not changeable.

## How do I highlight links?

- A link is a link between hubs, a verb. Examples can be - any business event, purchase, sale, exchange, order, etc.

## How did I isolate the satellites?

- Satilite is an adjective that describes the properties of zabs or links. Contains the key of the hub or link. 
Almost always historical (therefore dates from date/to date - for SCD 2)

An example of my model is below:
![data_vault](https://user-images.githubusercontent.com/55916170/187229547-040de9a0-75b5-4e77-8d5c-834c900a31ba.png)
