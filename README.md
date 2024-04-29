# vendor-management-system

A system for vendor management. Assignment given by Fatmug Designs

### Setup

- To set this up in your own local machine, first create a folder

```
mkdir vendor-management-system
cd vendor-management-system
```

- Clone the repo in the folder

```
> git clone https://github.com/amoeba25/vendor-management-system.git
```

- Next, create a virtual environment, activate it and install all the dependencies in the requirements.txt

```
> python -m venv "vendor_venv"
> vendor_venv/Scripts/activate.bat
> pip install requirements.txt
```

- Once this process is done, the setup is complete. We can either look at different api paths with "/api" or look at the documentation at the path "/swagger"

### Approaches

- Here when creating a vendor, we will just need to add the name, address and contact details of the vendor with other fields being hidden (only used for analysis and a unique vendor_code is created at the time of saving the instance)
- For the purchase order number, we have created it to be a read only field so that it is created automatically on saving the model. Here all purchase_order numbers are created with the prefix of "PO_random_str"
- Timezone changed to IST
- Added Swagger UI for a proper documentation of all the APIs

### Improvisations

Although the project is built on certain, pre-defined requirements there is a scope for improvising it. Here are certain suggestions I would change or make

- Add validation to the Vendor Model class

  ```
  class Vendor(models.Model):
      """
      Stores essential information about each vendor and their performance metrics.
      """

      name = models.CharField(max_length=250, help_text="Name of the vendor")
      contact_details = models.TextField(help_text="Contact details of the vendor")
      address = models.TextField(help_text="Address of the vendor")
      vendor_code = models.CharField(unique=True, max_length=10, help_text="Unique vendor code")
      on_time_delivery_rate = models.FloatField(help_text="On-time delivery rate", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
      quality_rating_avg = models.FloatField(help_text="Average quality rating", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
      average_response_time = models.FloatField(help_text="Average response time (in hours)", validators=[MinValueValidator(0.0)])
      fullfillment_rate = models.FloatField(help_text="Fulfillment rate", validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
  ```

- Adding indexing to the PO for faster quering of data

  ```
  from django.db import models
  from vendor.models import Vendor  # Assuming Vendor model is defined in vendor app

  class PurchaseOrder(models.Model):
      """
      Details of each purchase order and is used to calculate
      various performance metrics
      """
      # all model fields added

      class Meta:
          indexes = [
              models.Index(fields=['po_number']),
              models.Index(fields=['order_date']),
              models.Index(fields=['delivery_date']),
          ]

      def __str__(self):
          return self.po_number
  ```

- Could make the rating a scale from 1 to 5 rather than a float field in the purchase order model
- Average response time for each vendor, is calculated in hours and stored
