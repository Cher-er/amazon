两张表需要存储的属性：

- review
  
  - 'overall'
  - 'reviewTim'
  - 'reviewerID'
  - 'asin'
  - 'reviewerName'
  - 'reviewText'
  - 'summary'
  - 'unixReviewTime'
  
- metadata

  - 'category': list -> category(cate_id, category), meta_cate(asin, cate_id)

  - 'description': list -> description(asin, description)

  - 'title'

  - 'also_buy': list asin -> also_buy(asin, buy_asin)

  - 'brand'

  - 'feature': list -> feature(asin, feature:str)

  - 'rank'

  - 'also_view': list asin -> also_buy(asin, asin)

  - 'main_cat'

  - 'price'

  - 'asin'