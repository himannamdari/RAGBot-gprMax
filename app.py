import os
import streamlit as st
import logging
import re

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
        "Explain the Peplinski soil model",
        "How do antenna models work in gprMax?",
        "What are the steps to create a B-scan?",
    ]
    
    for q in example_questions:
        if st.button(q):
            st.session_state["user_input"] = q
            st.rerun()

# This is an enhanced demo version that better simulates RAG behavior
class EnhancedRAGEngine:
    """A enhanced RAG engine that returns knowledge-based responses for demo purposes."""
    
    def __init__(self):
        # Initialize knowledge base with content from gprMax documentation
        self.knowledge_base = {
            "install": {
                "content": """To install gprMax, follow these steps:

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
  ```

For GPU acceleration, you'll need to install the NVIDIA CUDA Toolkit and the pycuda Python module.""",
                "metadata": {"section": "Getting Started", "page": "4-7"}
            },
            "essential commands": {
                "content": """The essential commands required to run any gprMax model are:

1. `#domain`: Specifies the size of the model (in meters), e.g., `#domain: 0.5 0.5 1.0`

2. `#dx_dy_dz`: Specifies the spatial discretization (in meters), e.g., `#dx_dy_dz: 0.001 0.001 0.001`

3. `#time_window`: Specifies the total simulation time (in seconds), e.g., `#time_window: 20e-9`

Without these commands, gprMax will terminate execution and issue an appropriate error message. All other commands (materials, object construction, sources, etc.) are optional but necessary for creating useful models.""",
                "metadata": {"section": "Input file commands", "page": "22"}
            },
            "heterogeneous soil": {
                "content": """To model a heterogeneous soil in gprMax, you can use the `#fractal_box` command combined with a soil mixing model.

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
                "metadata": {"section": "Advanced features", "page": "115-117"}
            },
            "pml": {
                "content": """The Perfectly Matched Layer (PML) is an absorbing boundary condition used in gprMax to simulate open boundary problems like GPR. 

The PML absorbs waves impinging on the boundaries of the computational domain, preventing unwanted reflections. gprMax uses a PML based on a recursive integration approach to the complex frequency shifted (RIPML) formulation.

By default, gprMax uses 10 cells of PML on all six sides of the model domain. You can control this using the `#pml_cells` command:

```
#pml_cells: 10 10 20 10 10 20
```

This sets the PML thickness for each boundary (x0, y0, z0, xmax, ymax, zmax). You can set any thickness to zero to turn off the PML on that boundary.

For advanced users, the `#pml_cfs` command allows customization of the PML parameters for better performance in specific applications.""",
                "metadata": {"section": "Absorbing boundary conditions", "page": "19-20"}
            },
            "visualize results": {
                "content": """To visualize results in gprMax, you have several options:

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
                "metadata": {"section": "Plotting", "page": "49-50"}
            },
            "peplinski soil model": {
                "content": """The Peplinski soil model in gprMax is a semi-empirical mixing model that describes the dielectric properties of soils. It was initially suggested by Dobson et al. and adapted by Peplinski, and is valid for frequencies in the range 0.3GHz to 1.3GHz.

The model is implemented through the `#soil_peplinski` command with syntax:

```
#soil_peplinski: f1 f2 f3 f4 f5 f6 str1
```

Where:
- f1 is the sand fraction (0-1)
- f2 is the clay fraction (0-1)
- f3 is the bulk density in g/cm³
- f4 is the sand particle density in g/cm³
- f5 and f6 define a range for volumetric water fraction
- str1 is an identifier for the soil

For example:
```
#soil_peplinski: 0.5 0.5 2.0 2.66 0.001 0.25 my_soil
```

The model relates relative permittivity of the soil to bulk density, sand particle density, sand fraction, clay fraction and water volumetric fraction. The real and imaginary parts of this semi-empirical model can be approximated using a multi-pole Debye function plus a conductive term.

This approach is typically used with the `#fractal_box` command to create soils with more realistic dielectric and geometric properties.""",
                "metadata": {"section": "Material commands", "page": "26-27"}
            },
            "antenna models": {
                "content": """gprMax includes Python modules with pre-defined models of antennas that behave similarly to commercial antennas. Currently, models similar to GSSI 1.5 GHz, GSSI 400 MHz, and MALA 1.2 GHz antennas are included.

To use an antenna model in your simulation, you can access it via Python scripting in your input file:

```python
#python:
from user_libs.antennas.GSSI import antenna_like_GSSI_1500
antenna_like_GSSI_1500(0.125, 0.094, 0.100, resolution=0.002)
#end_python:
```

The antenna models are inserted at location x,y,z specified in the function. The coordinates are relative to the geometric center of the antenna in the x-y plane and the bottom of the antenna skid in the z direction.

The models must be used with cubic spatial resolutions of either 0.5mm (GSSI 400MHz antenna only), 1mm (default), or 2mm by setting the optional resolution parameter.

You can also rotate the antenna models 90 degrees counter-clockwise in the x-y plane by setting the optional rotate90=True parameter.""",
                "metadata": {"section": "GPR antenna models", "page": "69-73"}
            },
            "b-scan": {
                "content": """A B-scan is composed of multiple A-scans (traces) recorded as the source and receiver are moved over a target. To create a B-scan in gprMax, you need to:

1. Create a model with source and receiver that can be moved between model runs:
```
#hertzian_dipole: z 0.040 0.170 0 my_ricker
#rx: 0.080 0.170 0
#src_steps: 0.002 0 0
#rx_steps: 0.002 0 0
```

2. Use the -n command line option to specify the number of model runs (A-scans):
```
python -m gprMax user_models/my_bscan.in -n 60
```

3. After the simulation, merge the individual A-scan output files:
```
python -m tools.outputfiles_merge user_models/my_bscan
```

4. Visualize the B-scan:
```
python -m tools.plot_Bscan user_models/my_bscan_merged.out Ez
```

For more complex models, you can move the antenna using Python code in the input file with the current_model_run variable.""",
                "metadata": {"section": "B-scan from a metal cylinder", "page": "104-105"}
            },
            "overview": {
                "content": """gprMax is open source software that simulates electromagnetic wave propagation. It solves Maxwell's equations in 3D using the Finite-Difference Time-Domain (FDTD) method. gprMax was designed for modelling Ground Penetrating Radar (GPR) but can also be used to model electromagnetic wave propagation for many other applications.

Key features include:
1. Python scriptable input files
2. Built-in library of antenna models
3. Anisotropic material modelling
4. Dispersive material modelling using multiple pole Debye, Lorentz or Drude formulations
5. Building heterogeneous objects using fractal distributions
6. Building objects with rough surfaces
7. Modelling soils with realistic dielectric and geometric properties
8. Improved PML (RIPML) performance
9. OpenMP/MPI parallelization and GPU acceleration

The software is principally written in Python with performance-critical parts written in Cython and CUDA.""",
                "metadata": {"section": "Introduction", "page": "1-3"}
            }
        }
        
        # Add additional keywords for better matching
        self.keyword_mapping = {
            "installation": "install",
            "installing": "install",
            "setup": "install",
            "command": "essential commands",
            "soil": "heterogeneous soil",
            "peplinski": "peplinski soil model",
            "absorbing boundary": "pml",
            "perfectly matched layer": "pml", 
            "boundary condition": "pml",
            "visualize": "visualize results",
            "visualization": "visualize results",
            "plot": "visualize results",
            "antenna": "antenna models",
            "gssi": "antenna models",
            "mala": "antenna models",
            "b-scan": "b-scan",
            "bscan": "b-scan",
            "multiple traces": "b-scan"
        }
    
    def search_knowledge_base(self, query):
        """Search the knowledge base for relevant content based on the query."""
        query_lower = query.lower()
        
        # Check for direct matches in knowledge base
        for key in self.knowledge_base:
            if key in query_lower:
                return [self.knowledge_base[key]]
        
        # Check for keyword matches
        matches = []
        for keyword, topic in self.keyword_mapping.items():
            if keyword in query_lower and topic in self.knowledge_base:
                matches.append(self.knowledge_base[topic])
        
        # If matches found, return them
        if matches:
            return matches
        
        # No matches, return overview
        return [self.knowledge_base["overview"]]
    
    def generate_response(self, query):
        """Generate a response based on the query by searching the knowledge base."""
        # Search knowledge base
        retrieved_docs = self.search_knowledge_base(query)
        
        # Get content and sources
        content = "\n\n".join([doc["content"] for doc in retrieved_docs])
        sources = [f"Section: {doc['metadata']['section']}, Page: {doc['metadata']['page']}" for doc in retrieved_docs]
        
        # Return response
        return content, sources

# Initialize the RAG engine
@st.cache_resource
def initialize_rag_engine():
    return EnhancedRAGEngine()

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your GPRMax assistant. How can I help you with your Ground Penetrating Radar simulations today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize rag engine
rag_engine = initialize_rag_engine()

# User input
if "user_input" in st.session_state:
    user_input = st.session_state.user_input
    del st.session_state.user_input
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response using rag engine
    with st.chat_message("assistant"):
        with st.spinner("Searching documentation..."):
            response_container = st.empty()
            response, sources = rag_engine.generate_response(user_input)
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
    st.rerun()
