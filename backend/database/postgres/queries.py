class CameraQueries:

    CREATE_CAMERA = """

    INSERT INTO cameras
    (
        camera_id,
        sector_id,
        camera_type,
        stream_url,
        sensor_health
    )
    VALUES
    (
        :camera_id,
        :sector_id,
        :camera_type,
        :stream_url,
        :sensor_health
    )

    """

    GET_CAMERA = """

    SELECT *

    FROM cameras

    WHERE camera_id=:camera_id

    """


class RiskQueries:

    INSERT_RISK_EVENT = """

    INSERT INTO risk_events
    (
        sector_id,
        risk_level,
        risk_score,
        fusion_confidence,
        camera_type
    )
    VALUES
    (
        :sector_id,
        :risk_level,
        :risk_score,
        :fusion_confidence,
        :camera_type
    )

    """

    GET_RECENT_RISKS = """

    SELECT *

    FROM risk_events

    ORDER BY created_at DESC

    LIMIT 100

    """