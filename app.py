import os
import streamlit as st
import logging

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="GPRMax RAGBot",
    page_icon="📡",
    layout="wide"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Main title
st.title("📡 GPRMax RAGBot")
st.markdown("### Your AI assistant for GPR simulations")

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.info(
        """
        This AI assistant is trained on the gprMax documentation to help you:
        - Learn about gprMax features
        - Get guidance on model setup
        - Troubleshoot common issues
        - Understand GPR simulation concepts
        
        [gprMax Official Website](https://www.gprmax.com/)
        """
    )
    
    st.markdown("### Examples")
    example_questions = [
        "How do I install gprMax?",
        "What are the essential commands for input files?",
        "How do I model a heterogeneous soil?",
        "Explain the PML absorbing boundary conditions",
        "How can I visualize my results?",
    ]
    
    for q in example_questions:
        if st.button(q):
            st.session_state["user_input"] = q
            st.rerun()  # Updated from experimental_rerun()

# This is a demo version that simulates RAG behavior
class DemoRAGEngine:
    """A demo RAG engine that returns pre-defined responses for demonstration purposes."""
    
    def __init__(self):
        # Pre-defined responses for common questions
        self.demo_responses = {
            "install": {
                "response": """To install gprMax, follow these steps:

1. Install Python, required Python packages, and get the gprMax source code from GitHub
2. Install a C compiler which supports OpenMP
3. Build and install gprMax

The recommended approach is using Miniconda:
- Download and install Miniconda (Python 3.x version)
- Open a Terminal/Command Prompt and run:
  ```
  conda update conda
  conda install git
  git clone https://github.com/gprMax/gprMax.git
  cd gprMax
  conda env create -f conda_env.yml
  ```
- Build and install with:
  ```
  python setup.py build
  python setup.py install
  ```""",
                "sources": ["Section: Getting Started, Page: 4-7"]
            },
            "essential commands": {
                "response": """The essential commands required to run any gprMax model are:

1. `#domain`: Specifies the size of the model (in meters), e.g., `#domain: 0.5 0.5 1.0`

2. `#dx_dy_dz`: Specifies the spatial discretization (in meters), e.g., `#dx_dy_dz: 0.001 0.001 0.001`

3. `#time_window`: Specifies the total simulation time (in seconds), e.g., `#time_window: 20e-9`

Without these commands, gprMax will terminate execution and issue an appropriate error message. All other commands (materials, object construction, sources, etc.) are optional but necessary for creating useful models.""",
                "sources": ["Section: Input file commands, Page: 22"]
            },
            "heterogeneous soil": {
                "response": """To model a heterogeneous soil in gprMax, you can use the `#fractal_box` command combined with a soil mixing model.

First, define a soil mixing model using the Peplinski formula:
```
#soil_peplinski: 0.5 0.5 2.0 2.66 0.001 0.25 my_soil
```
This creates a soil with sand fraction 0.5, clay fraction 0.5, bulk density 2g/cm³, sand particle density of 2.66g/cm³, and volumetric water fraction range of 0.001-0.25.

Then create the heterogeneous soil volume using:
```
#fractal_box: 0 0 0 0.15 0.15 0.070 1.5 1 1 1 50 my_soil my_soil_box
```
This defines a box with fractal distribution (fractal dimension 1.5) using 50 different materials from the my_soil mixing model.

You can also add surface roughness with:
```
#add_surface_roughness: 0 0 0.070 0.15 0.15 0.070 1.5 1 1 0.065 0.080 my_soil_box
```""",
                "sources": ["Section: Advanced features, Page: 115-117"]
            },
            "PML": {
                "response": """The Perfectly Matched Layer (PML) is an absorbing boundary condition used in gprMax to simulate open boundary problems like GPR. 

The PML absorbs waves impinging on the boundaries of the computational domain, preventing unwanted reflections. gprMax uses a PML based on a recursive integration approach to the complex frequency shifted (RIPML) formulation.

By default, gprMax uses 10 cells of PML on all six sides of the model domain. You can control this using the `#pml_cells` command:

```
#pml_cells: 10 10 20 10 10 20
```

This sets the PML thickness for each boundary (x0, y0, z0, xmax, ymax, zmax). You can set any thickness to zero to turn off the PML on that boundary.

For advanced users, the `#pml_cfs` command allows customization of the PML parameters for better performance in specific applications.""",
                "sources": ["Section: Absorbing boundary conditions, Page: 19-20", "Section: PML commands, Page: 41-42"]
            },
            "visualize results": {
                "response": """To visualize results in gprMax, you have several options:

1. For A-scans (single traces), use the plot_Ascan.py module:
```
python -m tools.plot_Ascan outputfile
```

2. For B-scans (multiple traces), first merge the output files:
```
python -m tools.outputfiles_merge basefilename
```
Then plot the B-scan:
```
python -m tools.plot_Bscan outputfile rx-component
```

3. For geometry visualization, gprMax produces VTK files that can be viewed using Paraview:
- `.vti` files are created from the `#geometry_view` command
- `.vti` files are also created from the `#snapshot` command for viewing the propagation of the electromagnetic fields at specific time steps

4. For antenna parameters (input impedance, s11), use:
```
python -m tools.plot_antenna_params outputfile
```""",
                "sources": ["Section: Plotting, Page: 49-50", "Section: Output data, Page: 43-46"]
            }
        }
    
    def generate_response(self, query):
        """Generate a response based on the query."""
        query_lower = query.lower()
        
        # Check for keyword matches
        if "install" in query_lower:
            return self.demo_responses["install"]["response"], [self.demo_responses["install"]["sources"]]
        elif "essential" in query_lower or "command" in query_lower:
            return self.demo_responses["essential commands"]["response"], [self.demo_responses["essential commands"]["sources"]]
        elif "heterogeneous" in query_lower or "soil" in query_lower:
            return self.demo_responses["heterogeneous soil"]["response"], [self.demo_responses["heterogeneous soil"]["sources"]]
        elif "pml" in query_lower or "absorb" in query_lower or "boundary" in query_lower:
            return self.demo_responses["PML"]["response"], [self.demo_responses["PML"]["sources"]]
        elif "visual" in query_lower or "plot" in query_lower or "result" in query_lower:
            return self.demo_responses["visualize results"]["response"], [self.demo_responses["visualize results"]["sources"]]
        else:
            # Default response for other queries
            return """The gprMax documentation covers this topic in detail. Here are some key points about gprMax:

1. gprMax is open source software that simulates electromagnetic wave propagation for Ground Penetrating Radar (GPR) applications
2. It solves Maxwell's equations in 3D using the Finite-Difference Time-Domain (FDTD) method
3. The software allows building complex models with various materials, geometries, and sources
4. It supports both CPU (OpenMP) and GPU (CUDA) parallelization

Could you please try asking a more specific question about gprMax installation, commands, materials, object construction, or output visualization?""", ["Section: Introduction, Page: 1-3"]

# Initialize the demo RAG engine
@st.cache_resource
def initialize_demo_engine():
    return DemoRAGEngine()

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your GPRMax assistant. How can I help you with your Ground Penetrating Radar simulations today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize demo engine
demo_engine = initialize_demo_engine()

# User input
if "user_input" in st.session_state:
    user_input = st.session_state.user_input
    del st.session_state.user_input
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response using demo engine
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_container = st.empty()
            response, sources = demo_engine.generate_response(user_input)
            response_container.markdown(response)
            
            # If there are sources, display them
            if sources:
                st.markdown("#### Sources")
                for i, source in enumerate(sources, 1):
                    st.markdown(f"{i}. {source}")
    
    # Add assistant response to chat history
    full_response = response
    if sources:
        full_response += "\n\n**Sources:**\n" + "\n".join([f"{i}. {source}" for i, source in enumerate(sources, 1)])
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Input box for new questions
user_input = st.chat_input("Ask me about gprMax...")
if user_input:
    st.session_state.user_input = user_input
    st.rerun()  # Updated from experimental_rerun()
