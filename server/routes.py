"""
MF PipoNodes - Server Endpoints
API routes for Graph Plotter and Story Driver reset buttons
"""

from aiohttp import web
import server

from ..nodes import MF_GraphPlotter, MF_StoryDriver


@server.PromptServer.instance.routes.post("/graph_plotter/reset")
async def reset_graph_plotter(request):
    """Reset a Graph Plotter node's data."""
    try:
        data = await request.json()
        node_id = data.get("node_id")

        if not node_id:
            return web.json_response(
                {"success": False, "error": "node_id is required"}, status=400
            )

        MF_GraphPlotter.reset_node_data(node_id)

        return web.json_response(
            {"success": True, "node_id": node_id, "message": "Graph data reset"}
        )

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@server.PromptServer.instance.routes.post("/story_driver/reset")
async def reset_story_driver(request):
    """Reset a Story Driver step counter to 0."""
    try:
        data = await request.json()
        project_name = data.get("project_name", "MyProject")

        MF_StoryDriver.reset_project(project_name)

        return web.json_response(
            {"success": True, "project_name": project_name, "step": 0}
        )

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
