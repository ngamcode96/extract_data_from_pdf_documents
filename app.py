import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge 
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout


st.markdown(
    """
    <style>
    .react-flow__panel {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

nodes = [StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Node 1'}, node_type='input', source_position='bottom', draggable=True),
		StreamlitFlowNode('2', (0, 0), {'content': 'Node 2'}, 'default', 'bottom', 'top', draggable=True),
		StreamlitFlowNode('3', (0, 0), {'content': 'Node 3'}, 'default', 'bottom', 'top', draggable=True),
		StreamlitFlowNode('4', (0, 0), {'content': 'Node 4'}, 'output', target_position='top', draggable=True)]

edges = [StreamlitFlowEdge('1-2', '1', '2', animated=True),
		StreamlitFlowEdge('1-3', '1', '3', animated=False),
		StreamlitFlowEdge('2-4', '2', '4', animated=True, label="no", label_show_bg=True, label_bg_style={'stroke': 'white', 'fill': 'red'}),
		StreamlitFlowEdge('3-4', '3', '4', animated=True, label="yes", label_show_bg=True, label_bg_style={'stroke': 'white', 'fill': 'green'})]


if 'click_interact_state' not in st.session_state:
	st.session_state.click_interact_state = StreamlitFlowState(nodes, edges)

# if 'flow_state' not in st.session_state:
#     st.session_state.flow_state = StreamlitFlowState(nodes, edges)

# streamlit_flow('tree_layout', st.session_state.flow_state, layout=TreeLayout(direction='right'), fit_view=True)


updated_state = streamlit_flow('ret_val_flow',
				st.session_state.click_interact_state,
                height=800,
                layout=TreeLayout(direction='down'),
				fit_view=True,
				get_node_on_click=True,
				get_edge_on_click=True)


if updated_state.selected_id:
    for node in nodes:
        if node.id == updated_state.selected_id:
            st.write(f"Clicked on: {node.data['content']}")