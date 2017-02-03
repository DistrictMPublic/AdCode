#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleads import dfp
import csv

def main(client):
    # Initialize appropriate service.

    product_service = client.GetService('ProductService',version='v201611')

    # Create a statement to select products.

    statement = dfp.FilterStatement()

    # Retrieve a small amount of products at a time, paging
    # through until all products have been retrieved.

    print('product_status,product_id,product_name,targetedPlacementIds')

    with open('dfp_products.csv', 'wb') as csvfile:
        fieldnames = ['product_status', 'product_id', 'product_name', 'targetedPlacementIds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    while True:
        response = product_service.getProductsByStatement(statement.ToStatement())
        if 'results' in response:
            for product in response['results']:
                try:
                    for item in product.builtInTargeting.inventoryTargeting.targetedPlacementIds:
                        if product.productType == "DFP" and product.status == "ACTIVE":
                            print('%s,%d,%s,%s') % (product.status, product.id, product.name, item)
                            with open('dfp_products.csv', 'ab') as csvfile:
                                csv_writer = csv.writer(csvfile, delimiter=',')
                                csv_writer.writerow([product.status, product.id, product.name, item])
                except:
                    pass

            statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
            break

if __name__ == '__main__':
    # Initialize client object.

    dfp_client = dfp.DfpClient.LoadFromStorage()
    main(dfp_client)
