"""
VEGETA — Physical Labor Layer Skills
Virtuals Protocol ACP Provider — Robotics Automation Intelligence

40 skills backed by the 40 best AI robotics GitHub repos.
When hired, VEGETA researches, designs, and delivers robotics automation plans.

Layer: Physical Labor Layer (https://whitepaper.virtuals.io/about-virtuals/physical-labor-layer)
Protocol: ERC-8183 ACP — VEGETA as PROVIDER
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillResult:
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    @property
    def output(self) -> str:
        return json.dumps(self.data, ensure_ascii=False, indent=2) if self.success else self.error


# ── GitHub repo metadata fetcher ──────────────────────────────────────────────

def _fetch_github_repo(owner: str, repo: str) -> dict:
    import os
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"User-Agent": "VEGETA-ACP/1.0"}
    if token := os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return {
                "repo": f"{owner}/{repo}",
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "description": data.get("description", ""),
                "language": data.get("language", ""),
                "last_updated": data.get("updated_at", ""),
                "url": data.get("html_url", ""),
                "topics": data.get("topics", []),
            }
    except Exception as e:
        return {"repo": f"{owner}/{repo}", "error": str(e)}


def _fetch_arxiv(query: str, max_results: int = 5) -> list[dict]:
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/search/?query={encoded}&searchtype=all&max_results={max_results}"
    req = urllib.request.Request(url, headers={"User-Agent": "VEGETA-ACP/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode("utf-8")
            # Extract titles from Atom XML
            titles = []
            for chunk in content.split("<title>")[1:]:
                title = chunk.split("</title>")[0].strip()
                if title and "arxiv" not in title.lower():
                    titles.append(title)
            return [{"title": t} for t in titles[:max_results]]
    except Exception as e:
        return [{"error": str(e)}]


# ── Base class ────────────────────────────────────────────────────────────────

class RoboticsSkill:
    """
    VEGETA Physical Labor Layer — 40 robotics automation skills.
    Each skill returns a structured plan, research, or configuration
    backed by the corresponding GitHub repo ecosystem.
    """

    SKILL_ID = "vegeta_robotics_v1"
    SKILL_NAME = "VEGETA Robotics Intelligence"
    SKILL_DESCRIPTION = (
        "Physical Labor Layer provider. 40 robotics automation skills "
        "spanning manipulation, navigation, simulation, LLM-robotics, "
        "computer vision, and robot control. Backed by the top 40 AI robotics "
        "GitHub repos from Google DeepMind, Berkeley, CMU, MIT, NVIDIA, HuggingFace."
    )

    OFFERINGS: dict[str, dict] = {
        "roboticsRepoScan":      {"repo": ("huggingface", "lerobot"),          "price": 0.15},
        "graspPlannerSetup":     {"repo": ("BerkeleyAutomation", "dex-net"),   "price": 0.20},
        "navStackSetup":         {"repo": ("ros-planning", "navigation2"),     "price": 0.15},
        "objectDetectionPipeline":{"repo": ("ultralytics", "ultralytics"),     "price": 0.15},
        "segmentationMaskPlan":  {"repo": ("facebookresearch", "segment-anything"), "price": 0.15},
        "diffusionPolicyDesign": {"repo": ("columbia-ai-robotics", "diffusion_policy"), "price": 0.25},
        "physicsSimConfig":      {"repo": ("Genesis-Embodied-AI", "Genesis"),  "price": 0.20},
        "gpuSimTraining":        {"repo": ("isaac-sim", "IsaacLab"),           "price": 0.25},
        "rlEnvDesign":           {"repo": ("google-deepmind", "dm-control"),   "price": 0.20},
        "batchSimStrategy":      {"repo": ("google", "brax"),                  "price": 0.20},
        "embodiedNavPlan":       {"repo": ("facebookresearch", "habitat-sim"), "price": 0.20},
        "openXDataQuery":        {"repo": ("google-deepmind", "open_x_embodiment"), "price": 0.15},
        "foundationPolicyEval":  {"repo": ("Physical-Intelligence", "openpi"), "price": 0.25},
        "taskMotionPlan":        {"repo": ("caelan", "pddlstream"),            "price": 0.25},
        "unitreeDeployPlan":     {"repo": ("unitreerobotics", "unitree_sdk2_python"), "price": 0.25},
        "moveit2ArmPlan":        {"repo": ("moveit", "moveit2"),               "price": 0.20},
        "ros2NodeDesign":        {"repo": ("ros2", "ros2"),                    "price": 0.15},
        "droneWaypointPlan":     {"repo": ("microsoft", "AirSim"),             "price": 0.20},
        "autoSceneDesign":       {"repo": ("carla-simulator", "carla"),        "price": 0.20},
        "rlPolicyOptimize":      {"repo": ("google-deepmind", "acme"),         "price": 0.20},
        "alohaSetupGuide":       {"repo": ("tonyzhaozh", "aloha"),             "price": 0.20},
        "dexRetargetDesign":     {"repo": ("dexsuite", "dex-retargeting"),     "price": 0.20},
        "mobileRobotSetup":      {"repo": ("ROBOTIS-GIT", "turtlebot3"),       "price": 0.15},
        "stretchArmTask":        {"repo": ("hello-robot", "stretch_ros2"),     "price": 0.20},
        "ikSolverSetup":         {"repo": ("stephane-caron", "pink"),          "price": 0.15},
        "torqueCtrlLoop":        {"repo": ("kevinzakka", "torchcontrol"),      "price": 0.20},
        "pointCloudPipeline":    {"repo": ("facebookresearch", "pytorch3d"),   "price": 0.15},
        "pointEObjectGen":       {"repo": ("openai", "point-e"),               "price": 0.15},
        "florenceVLRobot":       {"repo": ("microsoft", "Florence-2"),         "price": 0.20},
        "humanoidSimPlan":       {"repo": ("kscalelabs", "sim"),               "price": 0.25},
        "robosuiteEnvSetup":     {"repo": ("ARISE-Initiative", "robosuite"),   "price": 0.15},
        "hulcLangSkill":         {"repo": ("mees", "hulc2"),                   "price": 0.25},
        "rtxPolicyScan":         {"repo": ("google-research", "robotics_transformer"), "price": 0.25},
        "pyroboSimTask":         {"repo": ("sea-bass", "pyrobosim"),           "price": 0.15},
        "gibsonHomeSim":         {"repo": ("iGibson-OSS", "iGibson"),         "price": 0.20},
        "pinocchioKDyn":         {"repo": ("stack-of-tasks", "pinocchio"),     "price": 0.20},
        "rlaxPolicyTrain":       {"repo": ("google-deepmind", "rlax"),         "price": 0.20},
        "robotLogAnalyze":       {"repo": ("foxglove", "mcap"),                "price": 0.15},
        "serlRLFinetune":        {"repo": ("rail-berkeley", "serl"),           "price": 0.25},
        "dexArtGraspPlan":       {"repo": ("dexsuite", "dexart-release"),      "price": 0.25},
    }

    def execute(self, offering_id: str, requirements: dict) -> SkillResult:
        """Route offering_id to the correct handler."""
        handler = getattr(self, f"_skill_{offering_id}", None)
        if handler is None:
            # Generic handler: fetch repo + arxiv context
            return self._generic_robotics_plan(offering_id, requirements)
        try:
            return handler(requirements)
        except Exception as e:
            return SkillResult(success=False, error=f"{offering_id} execution error: {e}")

    # ── Generic fallback ──────────────────────────────────────────────────────

    def _generic_robotics_plan(self, offering_id: str, req: dict) -> SkillResult:
        meta = self.OFFERINGS.get(offering_id, {})
        owner, repo = meta.get("repo", ("huggingface", "lerobot"))
        repo_data = _fetch_github_repo(owner, repo)
        arxiv_results = _fetch_arxiv(f"{repo} robotics", max_results=3)
        task = req.get("task", req.get("robot", req.get("goal", offering_id)))
        return SkillResult(
            success=True,
            data={
                "skill": offering_id,
                "task": task,
                "source_repo": repo_data,
                "related_papers": arxiv_results,
                "plan": self._build_plan(offering_id, task, repo_data),
                "requirements_received": req,
            },
        )

    def _build_plan(self, skill: str, task: str, repo: dict) -> dict:
        return {
            "objective": f"Automate '{task}' using {repo.get('repo', skill)} ecosystem",
            "stack": repo.get("language", "Python"),
            "steps": [
                f"1. Review {repo.get('url', '')} for relevant modules",
                f"2. Adapt implementation to target robot/task: {task}",
                "3. Configure simulation or hardware parameters",
                "4. Run validation suite and iterate",
                "5. Deploy to production environment",
            ],
            "estimated_complexity": "medium",
            "key_dependencies": repo.get("topics", [])[:5],
        }

    # ── Skill handlers ────────────────────────────────────────────────────────

    def _skill_roboticsRepoScan(self, req: dict) -> SkillResult:
        target = req.get("repo", "huggingface/lerobot")
        if "/" in target:
            owner, repo = target.split("/", 1)
        else:
            owner, repo = "huggingface", target
        repo_data = _fetch_github_repo(owner, repo)
        papers = _fetch_arxiv(f"{repo} robot learning", max_results=5)
        return SkillResult(success=True, data={
            "skill": "roboticsRepoScan",
            "target_repo": f"{owner}/{repo}",
            "repo_metadata": repo_data,
            "related_papers": papers,
            "integration_guide": {
                "install": f"pip install git+https://github.com/{owner}/{repo}.git",
                "key_entry_points": f"See {repo_data.get('url', '')}/tree/main",
                "topics": repo_data.get("topics", []),
                "stars": repo_data.get("stars", 0),
                "language": repo_data.get("language", "Python"),
            },
        })

    def _skill_graspPlannerSetup(self, req: dict) -> SkillResult:
        object_type = req.get("object", "generic rigid body")
        gripper = req.get("gripper", "parallel-jaw")
        repo = _fetch_github_repo("BerkeleyAutomation", "dex-net")
        return SkillResult(success=True, data={
            "skill": "graspPlannerSetup",
            "object": object_type,
            "gripper": gripper,
            "source_repo": repo,
            "pipeline": {
                "perception": "Point cloud from depth camera → surface normals",
                "grasp_sampling": f"Dex-Net 4.0 antipodal grasp candidates for {gripper}",
                "quality_metric": "Robust wrench space (RWS) + form closure",
                "execution": "Top-K grasp ranked by GQ-CNN score",
                "fallback": "Planar grasp if GQ-CNN confidence < 0.7",
            },
            "config": {
                "camera": "RealSense D435 or ZED 2 (depth @ 30fps)",
                "model": "gqcnn_4.0_pj (parallel-jaw) / gqcnn_4.0_suction",
                "threshold": 0.7,
                "point_cloud_downsample": 0.005,
            },
            "ros2_node": "dex_net_grasp_planner_node → /grasp_pose (geometry_msgs/PoseStamped)",
        })

    def _skill_navStackSetup(self, req: dict) -> SkillResult:
        robot = req.get("robot", "differential drive")
        environment = req.get("environment", "indoor")
        repo = _fetch_github_repo("ros-planning", "navigation2")
        return SkillResult(success=True, data={
            "skill": "navStackSetup",
            "robot": robot,
            "environment": environment,
            "source_repo": repo,
            "nav2_config": {
                "planner": "NavFn (Dijkstra) for structured; Smac Hybrid-A* for tight spaces",
                "controller": "DWB (differential drive) / MPPI (ackermann)",
                "costmap": {"global": "StaticLayer + InflationLayer", "local": "ObstacleLayer + VoxelLayer"},
                "slam": "SLAM Toolbox (online async mode)",
                "recovery": ["ClearCostmapRecovery", "SpinRecovery", "BackUpRecovery"],
            },
            "launch_sequence": [
                "ros2 launch nav2_bringup slam.launch.py",
                "ros2 launch nav2_bringup navigation.launch.py",
                "rviz2 -d nav2_default.rviz",
            ],
        })

    def _skill_objectDetectionPipeline(self, req: dict) -> SkillResult:
        target_classes = req.get("classes", ["person", "bottle", "cup"])
        robot_platform = req.get("platform", "ROS2")
        repo = _fetch_github_repo("ultralytics", "ultralytics")
        return SkillResult(success=True, data={
            "skill": "objectDetectionPipeline",
            "target_classes": target_classes,
            "platform": robot_platform,
            "source_repo": repo,
            "model_selection": {
                "edge_device": "YOLOv8n (nano) — 3.2ms, 6M params",
                "jetson": "YOLOv8s (small) — 7.2ms, 11.2M params",
                "workstation": "YOLOv8l (large) — 23ms, 43.7M params",
                "recommended": "YOLOv8s for robot with Jetson Orin",
            },
            "ros2_integration": {
                "node": "yolov8_ros2_node",
                "input_topic": "/camera/color/image_raw",
                "output_topic": "/detections (vision_msgs/Detection2DArray)",
                "fps_target": 30,
            },
            "custom_training": {
                "dataset_format": "YOLO format (images/ + labels/)",
                "epochs": 100,
                "imgsz": 640,
                "command": f"yolo detect train data=custom.yaml model=yolov8s.pt epochs=100",
            },
        })

    def _skill_diffusionPolicyDesign(self, req: dict) -> SkillResult:
        task = req.get("task", "pick and place")
        demos = req.get("num_demos", 100)
        repo = _fetch_github_repo("columbia-ai-robotics", "diffusion_policy")
        papers = _fetch_arxiv("diffusion policy robot manipulation", max_results=3)
        return SkillResult(success=True, data={
            "skill": "diffusionPolicyDesign",
            "task": task,
            "source_repo": repo,
            "related_papers": papers,
            "architecture": {
                "policy_type": "DDPM (denoising diffusion probabilistic model)",
                "backbone": "CNN (image input) or Transformer (state input)",
                "obs_horizon": 2,
                "action_horizon": 8,
                "prediction_horizon": 16,
                "noise_scheduler": "DDIM (accelerated inference, 10 steps)",
            },
            "data_collection": {
                "recommended_demos": demos,
                "format": "zarr dataset (obs/action/episode_ends arrays)",
                "observation": "RGB image(s) + robot proprioception",
                "action_space": "delta EEF pose (6-DOF) or joint angles",
                "collection_method": "SpaceMouse teleoperation or kinesthetic teaching",
            },
            "training": {
                "epochs": 3000,
                "batch_size": 256,
                "lr": 1e-4,
                "gpu_hours_estimate": f"{demos // 10} hrs on A100",
            },
        })

    def _skill_taskMotionPlan(self, req: dict) -> SkillResult:
        task = req.get("task", "stack blocks")
        objects = req.get("objects", ["block_A", "block_B", "table"])
        repo = _fetch_github_repo("caelan", "pddlstream")
        return SkillResult(success=True, data={
            "skill": "taskMotionPlan",
            "task": task,
            "objects": objects,
            "source_repo": repo,
            "tamp_plan": {
                "domain_predicates": ["On(x,y)", "Clear(x)", "Holding(x)", "Empty(gripper)"],
                "task_operators": ["pick(obj, pose)", "place(obj, surface, pose)"],
                "motion_streams": ["plan_motion(q1, q2) → trajectory", "sample_grasp(obj) → grasp_pose"],
                "goal": f"achieve {task} with optimal trajectory",
                "planner": "Adaptive (FF + motion planning iterations)",
            },
            "implementation_notes": [
                "Define geometry streams for collision-free IK",
                "Register all object bounding boxes in scene",
                "Use pddlstream.algorithms.adaptive for real-time replanning",
                "Integrate with MoveIt2 for motion execution",
            ],
        })

    def _skill_unitreeDeployPlan(self, req: dict) -> SkillResult:
        robot_model = req.get("robot", "Go2")
        mission = req.get("mission", "patrol and inspect")
        repo = _fetch_github_repo("unitreerobotics", "unitree_sdk2_python")
        return SkillResult(success=True, data={
            "skill": "unitreeDeployPlan",
            "robot": robot_model,
            "mission": mission,
            "source_repo": repo,
            "deployment": {
                "sdk": "unitree_sdk2_python (DDS-based, real-time)",
                "connection": "Ethernet (192.168.123.161) or WiFi",
                "latency": "< 5ms DDS publish-subscribe",
                "safety_limits": {"max_velocity": "1.5 m/s", "max_yaw_rate": "2.0 rad/s"},
            },
            "motion_primitives": {
                "locomotion": ["StandUp", "LayDown", "Move(vx,vy,vyaw)", "StopMove"],
                "arm_H1": ["MoveJ", "MoveL", "Grasp", "Release"],
                "sport_mode": ["Damping", "BalanceStand", "StairClimb"],
            },
            "mission_plan": {
                "objective": mission,
                "waypoints": "Defined via GPS/UWB or SLAM map coordinates",
                "perception": "Unitree L1 LiDAR + front camera",
                "autonomy_stack": "Nav2 + custom obstacle avoidance",
            },
        })

    def _skill_foundationPolicyEval(self, req: dict) -> SkillResult:
        task = req.get("task", "tabletop manipulation")
        robot = req.get("robot", "UR5e")
        repo = _fetch_github_repo("Physical-Intelligence", "openpi")
        papers = _fetch_arxiv("pi0 foundation policy robotics", max_results=3)
        return SkillResult(success=True, data={
            "skill": "foundationPolicyEval",
            "task": task,
            "robot": robot,
            "source_repo": repo,
            "related_papers": papers,
            "evaluation": {
                "policy": "π0 (Physical Intelligence openpi)",
                "input": "Language instruction + multi-view RGB images",
                "output": "Action tokens → robot joint targets / EEF deltas",
                "latency": "~50ms inference on A100",
                "supported_robots": ["ALOHA", "Franka", "UR5e", "xArm", "custom via URDF"],
            },
            "fine_tuning": {
                "demos_needed": f"50-200 task-specific demos for {task}",
                "method": "π0-FAST (action flow matching, full fine-tune)",
                "compute": "4× A100 GPUs, ~8h training",
                "checkpoint": "Hugging Face Hub (lerobot/π0 weights)",
            },
            "recommendation": f"π0 is {'highly suitable' if 'manipulation' in task.lower() else 'suitable with fine-tuning'} for {task}",
        })

    def _skill_ros2NodeDesign(self, req: dict) -> SkillResult:
        system = req.get("system", "mobile manipulation")
        nodes = req.get("nodes", ["perception", "planning", "control"])
        repo = _fetch_github_repo("ros2", "ros2")
        return SkillResult(success=True, data={
            "skill": "ros2NodeDesign",
            "system": system,
            "source_repo": repo,
            "architecture": {
                "nodes": {n: {"type": "rclpy.Node", "lifecycle": True, "qos": "reliable"} for n in nodes},
                "topics": {
                    "/camera/image": "sensor_msgs/Image (10Hz)",
                    "/odom": "nav_msgs/Odometry (100Hz)",
                    "/cmd_vel": "geometry_msgs/Twist (50Hz)",
                    "/joint_states": "sensor_msgs/JointState (100Hz)",
                    "/goal_pose": "geometry_msgs/PoseStamped (on-demand)",
                },
                "services": ["/compute_trajectory", "/grasp_object", "/move_home"],
                "actions": ["/navigate_to_pose", "/execute_trajectory"],
                "middleware": "DDS (CycloneDX recommended for low-latency)",
            },
            "package_structure": {
                f"{system.replace(' ', '_')}_bringup": "Launch files and configs",
                f"{system.replace(' ', '_')}_msgs": "Custom message/service definitions",
                f"{system.replace(' ', '_')}_core": "Core logic nodes",
            },
        })

    def _skill_rlEnvDesign(self, req: dict) -> SkillResult:
        task = req.get("task", "reach target")
        obs_type = req.get("obs_type", "proprioception")
        repo = _fetch_github_repo("google-deepmind", "dm-control")
        return SkillResult(success=True, data={
            "skill": "rlEnvDesign",
            "task": task,
            "obs_type": obs_type,
            "source_repo": repo,
            "env_spec": {
                "framework": "dm-control / MuJoCo 3.x",
                "observation_space": {
                    "proprioception": "joint_pos, joint_vel, EEF_pose",
                    "vision": "rgb_array (84×84×3) or depth",
                    "combined": "both (for sim-to-real transfer)",
                },
                "action_space": "continuous joint torques or delta EEF pose",
                "reward": {
                    "dense": f"distance_to_goal({task}) + gripper_contact_bonus",
                    "sparse": "1.0 if task_complete else 0.0",
                    "shaped": "dense until success_rate > 0.5, then sparse",
                },
                "reset": "Randomise initial config within workspace bounds",
            },
            "training_config": {
                "algorithm": "SAC (continuous) or PPO (discrete)",
                "steps": "5M for simple tasks, 20M+ for manipulation",
                "parallel_envs": 16,
            },
        })

    def _skill_gpuSimTraining(self, req: dict) -> SkillResult:
        task = req.get("task", "locomotion")
        robot = req.get("robot", "quadruped")
        repo = _fetch_github_repo("isaac-sim", "IsaacLab")
        return SkillResult(success=True, data={
            "skill": "gpuSimTraining",
            "task": task,
            "robot": robot,
            "source_repo": repo,
            "isaac_lab_config": {
                "num_envs": 4096,
                "device": "cuda:0",
                "physics_dt": 0.005,
                "render_dt": 0.02,
                "headless": True,
            },
            "training": {
                "algorithm": "RSL-RL (PPO) — built-in Isaac Lab",
                "max_iterations": 10000,
                "save_interval": 500,
                "log_interval": 10,
                "gpu_hours": f"~{2 if task == 'locomotion' else 8}h on A100",
            },
            "sim_to_real_gap": {
                "domain_randomization": ["friction", "mass", "motor_strength", "noise"],
                "actuation_model": "actuator_net or DC motor model",
                "delay": "action delay 2-4 dt steps (20-40ms)",
            },
        })

    def _skill_robotLogAnalyze(self, req: dict) -> SkillResult:
        log_topic = req.get("topic", "/all")
        anomaly = req.get("detect_anomaly", True)
        repo = _fetch_github_repo("foxglove", "mcap")
        return SkillResult(success=True, data={
            "skill": "robotLogAnalyze",
            "topic_filter": log_topic,
            "anomaly_detection": anomaly,
            "source_repo": repo,
            "analysis_plan": {
                "tool": "mcap CLI + Foxglove Studio",
                "commands": [
                    "mcap info recording.mcap",
                    f"mcap filter recording.mcap --include-topic {log_topic} -o filtered.mcap",
                    "mcap convert filtered.mcap --output filtered.bag",
                ],
                "metrics": ["message_rate", "latency_distribution", "drop_rate", "sensor_sync"],
                "anomalies": ["timestamp_jumps", "missing_frames", "nan_values", "out_of_range"] if anomaly else [],
                "visualization": "Open in Foxglove Studio (foxglove.dev) for 3D replay",
            },
        })

    # All remaining offerings use the generic handler above.
    # Add specialised handlers below as needed.
