def make_exe():
    dist = default_python_distribution()
    python_config = dist.make_python_interpreter_config()
    python_config.run_module = "linkcheck_gui"

    policy = dist.make_python_packaging_policy()
    policy.resources_location_fallback = "filesystem-relative:lib"

    exe = dist.to_python_executable(
        name="linkchecker-gui",
        packaging_policy=policy,
        config=python_config,
    )

    for resource in exe.pip_download(["PyQt6"]):
        resource.add_location = "filesystem-relative:lib"
        exe.add_python_resource(resource)

    exe.add_python_resources(exe.pip_install([CWD]))
    return exe

register_target("exe", make_exe)
resolve_targets()
