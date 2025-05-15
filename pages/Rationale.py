import streamlit as st
st.markdown(
    '''# 🎲 :rainbow[RefRandomiser]: A tool to split and randomise data''')

st.write('&nbsp;')  # empty line
st.markdown("## When to randomise your records")
st.write("In evidence synthesis the focus of our research is secondary data (our search results and the included studies).  As in primary research, it is sometime necessary to randomise our data. Search results are ordered by the tools we use, they may be in date or alphabetical order.  This means that a non-random selection of our records will not be representative of the whole set of records.")
st.write("Two circumstances where selecting a random sample of our deduplicated records is necessary include:")
st.write("1)	When a proportion of records are selected to test agreement between reviewers (usually 20%)")
st.write("2)	When an AI generated algorithm is being developed and tested.  In these circumstances, usually three sets of random records need to be selected in order to ensure that the tool is developed with reduced risk of overfitting, data leakage and biased evaluation.")
st.write("The RefRandomise tool can support both of these processes.")
st.write('&nbsp;')  # empty line

st.markdown("## Methods to develop and evaluate an AI Tool")
st.markdown("### Datasets when developing LLM-based methods")
st.write("LLMs don’t require a training dataset because they are already pre-trained. Instead, they require a smaller ‘Prompt development’ dataset to develop and adjust prompts, as well as a larger Test set to independently validate the prompts. ")
st.markdown("### Other AI training and evaluation scenarios")
st.write("Data scientists use a ‘Train, Validate, Test’ process when developing an AI tool to process data and make decisions (such as when automatically extracting study characteristics), especially when using machine-learning or older models based on transformers.")
st.write("1. Training Set: The Training stage requires developing potential tools on a set of studies where there has been a manual, human generated gold standard of screened or data extraction results. This stage requires the largest portion of  data (eg. 70%). The model learns from this data by adjusting its parameters to minimize errors. This can be likened to the study material for an exam.")
st.write("2. Validation Set: The Validation stage requires that the tools are tested on another, different set of records*. This set is used to check training progress, usually a smaller set of about 10%. After the model has learned from the training set,  the validation set  is used to adjust the model's hyperparameters (settings that control the learning process). This is equivalent to presenting students with a practice exam designed to test their knowledge of the study material they have been given. ")
st.write("3. Test Set: Finally, the test set is used to evaluate the model's performance. This data has never been seen by the model during training or validation and could be around 20% of the data. It's like the final exam that determines how well the model has learned. The test set provides an unbiased evaluation of the model's ability to generalize to new data.  The final Test stage requires that the tools are tested on yet another set of records. ")

st.markdown("## Why randomised splitting of the data matters?")
st.write("Failing to undertake the evaluation of an AI tool using these processes can result in a number of threats to the integrity and safety of models. The reasons that these stages must be developed on a new and unique set is akin to preparing a class of students for an exam and then presenting them with the practice paper in the actual exam. It will not give a true picture of how well they have learned the content, and able to apply their learning to new questions.  ")
st.markdown("   •**Avoid Overfitting**: By using separate datasets, you ensure the model doesn't just memorize the training data but learns to generalize from it.")
st.markdown("   •**Hyperparameter Tuning**:The validation set helps in tuning the model without biasing the final evaluation.")
st.markdown("   •**Reducing Evaluation Bias**: The test set provides a final assessment of the model's performance, with as little bias as possible.")

