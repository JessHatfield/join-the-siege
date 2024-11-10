from locust import HttpUser, task


class LoadTestDocumentClassificationEndpoint(HttpUser):
    host = "https://document-classification-service-260885586204.europe-west2.run.app"

    @task
    def load_test_classification_endpoint(self):
        file_path = f"drivers_license_1.jpg"
        endpoint = "/classify_file"

        with open(file_path, 'rb') as file_to_upload:
            # Prepare the files parameter for multipart/form-data
            files = {
                'file': ('file.jpg', file_to_upload, 'image/jpeg')
            }

            self.client.post(endpoint, files=files)
