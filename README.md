# Heron Coding Challenge - File Classifier

## My Solution

### Thoughts about my approach

I've chosen to use a zero-shot text classifier and a dockerized deployment via Google Cloud Run to tackle this challenge

I've also refactored the project to more easily support the addition of new industries + classification methods, and have also expanded test coverage

Finally, I've used locust to load test the solution at scale

At each stage I attempted to get the most bang for my buck, choosing technologies that would give me the most functionality for the least amount of time investment.

- Using a zero-shot classifier to avoid having to collect a dataset and train a model/trick a LLM into working with sensitive data
- Using Docker + Google Cloud Run + Terraform to abstract away much of the complexity around building infrastructure/allowing me to support a wide range of load cases
- Adding Sentry + structlog + google cloud logging to the project allowed me to greatly improve observability with minimal effort (30-40 mins of work)

This was project was complete over about two days of work. If I was stricter with time I would have focused on the zero-shot classifier approach and then manually hosted it via Google Cloud Run

Scope was deliberately extended by the decision to add terraform/load testing/experimentation with different classification options. 

I was keen to learn more about these areas, but this did mean I spent hours troubleshooting infrastructure issues and went down a dead-end trying to use LocalLama to classify sensitive text

Overall this was a great learning experience, and I'm excited to talk through it with you all!


### How does my solution tackle each problem area?

#### Classifying Poorly Named Files

- I chose to extract the text contents of files via Tesseract and then pipe this in into a text classifier powered by Daberta V3
- This allows us to classify files based on their text content, sidestepping the problem of poorly named files entirely
- Manual tests with the files in this repo worked well. The model was choosing the right label with a high degree of confidence (90%+)
- Utilising the models pre-existing understanding of language also means we can save time vs using an OCR + keyword tallying approach
- It also aids with adding new document types, Excel/word docs could be supported easily by rendering them as images then extracting text via OCR. Much quicker vs writing parsers for each file type

#### Scaling to new industries

- Because our model has a general understanding of language we (theoretically) don't need to train new models when expanding to new industries
- I've also refactored the app structure around the concept of industries and used a strategy pattern to implement our classifier, giving other engineers a clear path to follow when adding support for new industries
- This saves a heap of time vs training new classifiers and ensures that new industries are added in a maintainable/readable manner!
- To add a new industry we just subclass [DocumentClassifier](https://github.com/JessHatfield/join-the-siege/blob/79ec8ab8d78c2ca235e01d27dfed6132c55bc275/src/classifiers/base_classifier.py), define new [enums](https://github.com/JessHatfield/join-the-siege/blob/39d9774e30153ceb46a870401a3dce9d0c936ad1/src/classifiers/industries/finance_and_insurance_classifier.py#L15-L18) and add the classifier to our [classify_files](https://github.com/JessHatfield/join-the-siege/blob/39d9774e30153ceb46a870401a3dce9d0c936ad1/src/classifier.py#L34) function. This takes about 30 mins at most!

#### Processing larger volumes of documents

- Running my solution via Google Cloud Run gives us the ability to quickly scale horizontally and handle volatile loads
- I've tested the solution via locust, I could achieve a mean response time of 6 seconds across a load of 10 RPS (so about 860k responses daily) with a success rate of about 98%
- I was also able to 10X load from 1 RPS to 10 RPS whilst maintaining this mean response time with a reasonable degree of stability

 Load testing screenshot
 <img alt="Load testing results" src="/join-the-siege/locust_load_testing_results.png"/>



Areas for improvement

Response times
   - An average response time of 6 seconds might not be acceptable for direct usage in a synchronous customer facing flow
   - It's hard to say without better understanding load requirements/use cases/system architecture, how much of a drawback this ultimately is!
   - Our 95% percentile response time remains very high (18 seconds) but I suspect with further optimisation I could solve the bugs causing this
   - If our system load was more consistent/controllable, we could likely reduce outliers by keeping a number of containers live at all time to reduce cold-start times

Choice of classifier

   - This exercise is time constrained, using a zero-shot classifier meant I didn't have to spend valuable time training a custom classifier
   - I could also avoid having to generate/collect a large labelled dataset. However, this comes at the cost of CPU usage + slower response times
   - Google Cloud Run also stores our 2GB model file in RAM which then further inflates our cloud costs!
   - If I had access to HeronDatas datasets I'd likely have tried to train my own classifier to reduce resource costs + speed up response times

CI/CD

   - Currently  pushing to main triggers a new deployment via Google Cloud Build, giving us some degree of automation
   - However, the progress of build not visible to wider team, which adds a heap of confusion + friction to the process
   - Furthermore, we don't enforce test successes prior to deployment or enforce style standards either!
   - Given more time I could use github actions + slack alerts to enforce tests/style standards and make the whole deployment process monitorable

## Overview

At Heron, we’re using AI to automate document processing workflows in financial services and beyond. Each day, we handle over 100,000 documents that need to be quickly identified and categorised before we can kick off the automations.

This repository provides a basic endpoint for classifying files by their filenames. However, the current classifier has limitations when it comes to handling poorly named files, processing larger volumes, and adapting to new industries effectively.

**Your task**: improve this classifier by adding features and optimisations to handle (1) poorly named files, (2) scaling to new industries, and (3) processing larger volumes of documents.

This is a real-world challenge that allows you to demonstrate your approach to building innovative and scalable AI solutions. We’re excited to see what you come up with! Feel free to take it in any direction you like, but we suggest:


### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?
- How might you extend the classifier with additional technologies, capabilities, or features?


### Part 2: Productionising the Classifier 

- How can you ensure the classifier is robust and reliable in a production environment?
- How can you deploy the classifier to make it accessible to other services and users?

We encourage you to be creative! Feel free to use any libraries, tools, services, models or frameworks of your choice

### Possible Ideas / Suggestions
- Train a classifier to categorize files based on the text content of a file
- Generate synthetic data to train the classifier on documents from different industries
- Detect file type and handle other file formats (e.g., Word, Excel)
- Set up a CI/CD pipeline for automatic testing and deployment
- Refactor the codebase to make it more maintainable and scalable

## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?


## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.app
    ```

4. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```

5. Run tests:
   ```shell
    pytest
    ```

## Submission

Please aim to spend 3 hours on this challenge.

Once completed, submit your solution by sharing a link to your forked repository. Please also provide a brief write-up of your ideas, approach, and any instructions needed to run your solution. 
