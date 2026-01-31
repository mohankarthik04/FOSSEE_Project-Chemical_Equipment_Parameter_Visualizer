from django.db import models
import pandas as pd

class EquipmentData(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            df = pd.read_csv(self.file.path)

            self.summary = {
                "total_count": int(len(df)),
                "avg_flowrate": float(df['Flowrate'].mean()) if 'Flowrate' in df else None,
                "avg_pressure": float(df['Pressure'].mean()) if 'Pressure' in df else None,
                "avg_temperature": float(df['Temperature'].mean()) if 'Temperature' in df else None,
                "type_distribution": (
                    df['Type'].value_counts().to_dict() if 'Type' in df else {}
                )
            }

            super().save(update_fields=['summary'])

        except Exception as e:
            print("Error processing CSV:", e)

        records = EquipmentData.objects.all().order_by('-uploaded_at')

        if records.count() > 5:
            for old_record in records[5:]:
                old_record.file.delete(save=False)  
                old_record.delete()  

    def __str__(self):
        return f"Equipment Data {self.id} - {self.uploaded_at}"
