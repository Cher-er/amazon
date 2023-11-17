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

  - 'category': list -> category(cat_id, cate), meta_cat(asin, cat_id)
    
  - 'description': list?? -> str
    
    > description虽然是列表，但是只有一个元素，可以直接当作字符串存起来
    
  - 'title'
    
  - 'also_buy': list asin -> also_buy(asin, asin)
    
  - 'brand'
    
  - 'feature': list -> feature(asin, feature:str)
    
  - 'rank'
    
  - 'also_view': list asin -> also_buy(asin, asin)
    
  - 'main_cat'
    
  - 'price'
    
  - 'asin'