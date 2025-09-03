# smu-keywords-EDA-2025.R
# Name: Crystal Hollis
# Creation Date: August 23, 2025
# =============================================================================
# Dataset files:
# jobsheetmain2025.08.23.csv        csv containing all values from all jobs 

# =============================================================================
# Phase 1: Get the Data: Find and load data into a data frame.

# Install latest versions of R and RStudio from https://posit.co/download/rstudio-desktop/
# Install / Update packages

# 1. Setup workspace and libraries
# Confirming Directory:
getwd()
setwd("C:\\Programming\\SMU_Projects\\data") # PC # Copy paste filepath to folder with csv, add double backslashes
# setwd("/Users/magnamediaartsllc/GitHub/SMU_Projects/data") Mac
getwd()

# # Load libraries
library(tidyverse)    # data manipulation & ggplot2
# library(skimr)        # quick summaries #commented out for now
# library(janitor)      # cleaning column names #commented out for now
# library(DataExplorer) # automated EDA reports #commented out for now
#   
# 2. Load Data
# # Load your CSV
jobsheet <- read_csv("jobsheetmain2025.08.23.csv", col_names = FALSE)
print(jobsheet)
negsheet <- read_csv("photoprocessandcatalogcompletelayout2025.08.23.csv", col_names = FALSE)
print(negsheet)

# 3. Assign column names
# The csv exports from FileMaker will not initially have column names.
# Use the following to add it to the dataset.
# Note, make sure the Field export order matches the order below.
# the Field export order must either be exactly in this order OR you can
# simply copy paste the field to the order you want.
js_column_names <- c(
  "Account_Number", "Account_Number_2", "Attire", "Budget_Job_Type", 
  "Building_List", "Client", "Client_Disk_Needed", "Client_Email", 
  "Client_Images_Sent_To", "Client_Images_Sent_To_Email", "Client_Phone", 
  "Complexity_Job", "Created_By", "Created_Date", 
  "Event_Arrive_Start_End_Time", "Event_Contact_At_Event", "Event_Date", 
  "Event_Key_Images", "Event_Location", "Event_Start_End_Time", 
  "Fiscal_Year_Main_2015", "Job", "Job_Name", "Job_Notes", "Job_Number", 
  "Job_Type", "Keyword_Review", "Keywords_Copy", "Media_Archive_Link", 
  "Notes_Social_Needs", "Phase", "Phase_Text", "Photo_Need", "Photographer", 
  "Photographer_Initials", "Photos_Need_For", "Photoshoot_Info_Confirmed", 
  "Requestor_Email", "Requestor_Name", "Requestor_Phone", 
  "Requisition_Approver_1", "Requisition_Approver_2", "Requisition_Approver_3", 
  "Requisition_School_Area_2", "Requisition_School_Area_3", "Requisition_Vendor", 
  "School_Name", "Staff_Internal_External", "Time_Estimate", "Type_Of_Project", 
  "JobCatalog_Phase_Production", "JobCatalog_Negative_Number", 
  "JobCatalog_Photo_Video_Project", "JobsDetails_Assignment_Details", 
  "JobsDetails_Assistant_Initials", "JobsDetails_Date_Of_Shoot",
  "JobsDetails_Date_To_Client", "JobsDetails_Keyword_Checker",  
  "JobsDetails_Photographer", "JobsDetails_Photographer_1", 
  "JobsDetails_Photographer_2", "JobsDetails_Photographer_3", 
  "JobsDetails_Photographer_4", "JobsDetails_Photographer_5", 
  "JobsDetails_Time", "PhotographyCatalog_Negative_Or_Slide_Number"
)

names(jobsheet) <- js_column_names

ns_column_names <- c(
  "Negative_Number", "Job_Number", "Job_Name", "Box_date_upload", 
  "checkbox_production", "checked_out_to_freelancer", "Complexity_folder",
  "Crooze_date_upload", "Date_external_gallery_created_in_PhotoShelter",
  "Date_upload_to_Photoshelter", "delete_from_Box", "Deleted_from_Media_Archive",
  "delivered_to_client", "DNGS_made", "Edited_processing", "Event_Date",
  "For_Crooze", "For_photoshelter", "For_Photoshelter_DAM",
  "For_Photoshelter_DAM_Ex_Upload", "heros_selected", "In_Box_confirmation_folder",
  "In_Crooze_confirmation_folder", "in_folder", "In_Media_Archive_confirmation",
  "job_phase_production", "Keyword_Check", "Keyword_Sent", "Keywords_catalog_process",
  "MA_date_upload", "Model_release_file", "Neg_Number_is_Final_Video", 
  "Photo_Video_project", "Photographer_Initials", "photoshelter_galleries",
  "Photoshelter_Upload_Quantity", "Priority_Level", "Public_Access", "quality_check_metadata",
  "Re_edited", "Reloaded_to_Media_Archive", "seconds_deleted", "seconds_moved_to_Box",
  "Seconds_ready_for_Box", "seconds_reviewed", "Sent_to_University_Archives",
  "Time_estimate", "Time_Freelance_Post_production", "Time_Photographer", 
  "Time_Postproduction", "Time_Postproduction_photographer", "to_production", 
  "upload_DEA_Box_ready", "upload_to_Box", "Upload_to_cruise", "upload_to_Media_archived", 
  "upload_to_production", "Jobs_Files_recieved", "Jobs_Fiscal_Year_main_2015"
)

names(negsheet) <- ns_column_names

# make sure your name vectors match the column counts
ncol(jobsheet); length(js_column_names)
ncol(negsheet); length(ns_column_names)

# 4. Summarize Data
# first 6 rows x first 17 columns
head(jobsheet)
head(negsheet)

# last 6 rows x first 17 columns - columns first row
tail(jobsheet)
tail(negsheet)

# first 22 rows x all columns - columns first column instead of row
glimpse(jobsheet)
glimpse(negsheet)

# 5. Understand the Data
# Check size, structure, missing values
# Number of rows and number of columns
dim(jobsheet)
dim(negsheet)

# Column names - make sure it matches what was done in step 3
colnames(jobsheet) 
colnames(negsheet)

# Structural snapshot
# Key:  $ Column Name - Column Name
#       chr / logi / num - Data type (character (string, text), logic (true, false, or NA), numeric (integers or doubles))
#       [1:26976] - number of entries
#       NA, "dates", "names" etc. - example values
str(jobsheet)
str(negsheet)

# Phase 2: Clean the Data: Fix missing values, adjust data types, remove unnecessary data.
# 1. Clean Data
# Standardize numeric in both Job_Numbers
jobsheet_subset <- jobsheet %>%
  mutate(Job_Number = as.character(Job_Number))

negsheet_subset <- negsheet %>%
  mutate(Job_Number = as.character(Job_Number))

library(stringr)
library(tidyr)
library(readr)
library(dplyr)

# Remove export artifacts from Job_Number just in case
jobsheet_subset <- jobsheet_subset %>%
  mutate(Job_Number = str_replace_all(Job_Number, "\\\\v", "") |> str_squish())

negsheet_subset <- negsheet_subset %>%
  mutate(Job_Number = str_replace_all(Job_Number, "\\\\v", "") |> str_squish())

# Small cleaner for keyword text
clean_kw <- function(x) {
  x %>%
    str_replace_all("\\\\v|\\\\035", " ") %>%  # strip control codes
    str_replace_all("\\s+", " ") %>%           # collapse spaces
    str_replace_all("^\\s+|\\s+$", "") %>%     # trim
    str_to_lower()
}


# skipping further adjustments for now


# Phase 3: Prepare the Data
# Create new calculated fields, transform data into required formats.
# 1. Select only the columns you want to work with

jobsheet_subset <- jobsheet %>%
  select(
    Job_Number,
    Job_Name,
    Job,
    Job_Type,
    Fiscal_Year_Main_2015,
    Event_Date,
    Event_Location,
    Keyword_Review,
    Keywords_Copy,
    Photo_Need,
    Photos_Need_For,
    School_Name,
    Time_Estimate,
    Staff_Internal_External,
    Type_Of_Project
  )

glimpse(jobsheet_subset)

negsheet_subset <- negsheet %>%
  select(
    Photographer_Initials, Job_Number, Negative_Number, Job_Name, Photo_Video_project,
    Event_Date, job_phase_production, Box_date_upload, Date_upload_to_Photoshelter,
    Keyword_Check, Keywords_catalog_process
  )

glimpse(negsheet_subset)

# 2. Unified keyword table
# Long form keywords from both sheets
kw_long <- bind_rows(
  jobsheet_subset %>%
    select(Job_Number, Job_Name, Source = Type_Of_Project, Keywords = Keywords_Copy),
  negsheet_subset %>%
    select(Job_Number, Job_Name, Source = Photo_Video_project, Keywords = Keywords_catalog_process)
) %>%
  mutate(Keywords = clean_kw(Keywords)) %>%
  # split on commas/semicolons/pipes and the literal text "location:" or "optional:" markers
  separate_rows(Keywords, sep = "\\s*,\\s*|\\s*;\\s*|\\s*\\|\\s*") %>%
  mutate(Keywords = str_remove_all(Keywords, "^(location:|optional:)\\s*")) %>%
  mutate(Keywords = str_squish(Keywords)) %>%
  filter(!is.na(Keywords), Keywords != "")
write_csv(kw_long, "keyword_unified_2025_08_23.csv")
 

# Phase 4: Analyze the Data: Summarize, visualize, and model the data.
# 1. Count top 25 keywords

# jobsheet
jobsheet_subset %>%
  filter(!is.na(Keywords_Copy)) %>%
  separate_rows(Keywords_Copy, sep = ",") %>%      # split on commas
  mutate(Keywords_Copy = str_trim(Keywords_Copy)) %>%  # trim whitespace
  count(Keywords_Copy, sort = TRUE) %>%
  slice_head(n = 25) %>%
  ggplot(aes(x = reorder(Keywords_Copy, n), y = n)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(title = "Top 25 Keywords in Jobsheet",
       x = "Keyword",
       y = "Count")

# negsheet
negsheet_subset %>%
  filter(!is.na(Keywords_catalog_process)) %>%
  separate_rows(Keywords_catalog_process, sep = ",") %>%
  mutate(Keywords_catalog_process = str_trim(Keywords_catalog_process)) %>%
  count(Keywords_catalog_process, sort = TRUE) %>%
  slice_head(n = 25) %>%
  ggplot(aes(x = reorder(Keywords_catalog_process, n), y = n)) +
  geom_col(fill = "darkred") +
  coord_flip() +
  labs(title = "Top 25 Keywords in Negsheet",
       x = "Keyword",
       y = "Count")

# Frequency table
kw_freq <- kw_long %>%
  count(Keywords, sort = TRUE, name = "freq")

glimpse(kw_freq)      # quick look
write_csv(kw_freq, "keyword_frequency_2025_08_23.csv")

# Compare to structured keywords
taxonomy <- read_lines("SMUKeywords_08.05.25.txt") %>%
  str_trim() %>%
  str_to_lower() %>%
  str_remove_all("\\[|\\]") %>% 
  discard(~ .x == "") %>%
  unique()

# Rogue = used in data but not in taxonomy
rogue_kw <- kw_freq %>%
  filter(!Keywords %in% taxonomy) %>%
  arrange(desc(freq))
write_csv(rogue_kw, "rogue_keywords_2025_08_23.csv")

# Unused = in taxonomy but never used in data
unused_kw <- setdiff(taxonomy, kw_freq$Keywords) %>%
  tibble(keyword = .) %>%
  arrange(keyword)
write_csv(unused_kw, "unused_taxonomy_2025_08_23.csv")

# Per‑source usage (photo vs video)
kw_by_source <- kw_long %>%
  count(Source, Keywords, sort = TRUE, name = "freq")
write_csv(kw_by_source, "keyword_by_source.csv")

# Per‑school usage (if present)
kw_by_school <- jobsheet_subset %>%
  select(Job_Number, School_Name) %>%
  left_join(kw_long, by = "Job_Number") %>%
  filter(!is.na(School_Name), School_Name != "") %>%
  count(School_Name, Keywords, sort = TRUE, name = "freq")
write_csv(kw_by_school, "keyword_by_school.csv")

# Suggested fixes for top rogue kws
# install.packages("stringdist") 
library(stringdist)

suggest_match <- function(term, vocab, n = 3) {
  d <- stringdist::stringdist(term, vocab, method = "osa")
  tibble(candidate = vocab, dist = d) %>% arrange(dist) %>% slice_head(n = n)
}

# Example: get suggestions for the top 10 rogue terms
rogue_suggestions <- rogue_kw %>%
  slice_head(n = 10) %>%
  rowwise() %>%
  mutate(suggestions = list(suggest_match(Keywords, taxonomy, n = 5))) %>%
  unnest(suggestions)

write_csv(rogue_suggestions, "rogue_suggestions.csv")


# Phase 5: Present the Data: Communicate findings effectively using visualizations.

