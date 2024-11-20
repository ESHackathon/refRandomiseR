library(shiny)
library(synthesisr)
library(dplyr)
library(bslib)

ui <- fluidPage(
  theme = bs_theme(
    version = 5,
    bg = "#008080", # Teal background
    fg = "white",   # White text
    primary = "#ffffff" # Optional: White primary components
  ),
  titlePanel("refRandomiseR"),
  
  sidebarLayout(
    sidebarPanel(
      fileInput("ris_file", "Upload RIS File", accept = ".ris"),
      radioButtons("subset_type", "Subset by:",
                   choices = c("Percentage" = "percentage", "Number of Records" = "number")),
      numericInput("subset_value", "Enter Value:", value = 10, min = 1),
      actionButton("subset", "Subset Records")
    ),
    
    mainPanel(
      tableOutput("subset_results"),
      downloadButton("download_subset", "Download Subset")
    )
  )
)

server <- function(input, output, session) {
  
  records <- reactiveVal(NULL)
  
  observeEvent(input$ris_file, {
    req(input$ris_file)
    # Read RIS file
    ris_data <-synthesisr::read_refs(input$ris_file$datapath)
    records(as.data.frame(ris_data))
  })
  
  subsetted_records <- eventReactive(input$subset, {
    req(records())
    data <- records()
    
    if (input$subset_type == "percentage") {
      # Subset by percentage
      n <- ceiling((input$subset_value / 100) * nrow(data))
    } else {
      # Subset by number
      n <- min(input$subset_value, nrow(data))
    }
    
    data[sample(nrow(data), n), ]
  })
  
  output$subset_results <- renderTable({
    subsetted_records()
  })
  
  output$download_subset <- downloadHandler(
    filename = function() {
      "subset_records.ris"
    },
    content = function(file) {
      req(subsetted_records())
      ris_out <- write_refs(subsetted_records(), format = "ris", file = FALSE) 
      writeLines(ris_out, file)
    }
  )
}

shinyApp(ui, server)
