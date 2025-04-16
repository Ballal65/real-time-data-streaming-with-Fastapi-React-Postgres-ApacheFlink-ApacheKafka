from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime, timedelta
router = APIRouter(tags=['JRE API'], prefix='/jre')

@router.get('/available-dates', status_code=status.HTTP_200_OK)
async def get_available_dates(db: Session = Depends(get_db)):
    try:
        query = text("""SELECT DISTINCT extraction_date FROM jre_insights_table ORDER by extraction_date;""")
        results = db.execute(query).fetchall()
        return [row.extraction_date for row in results]
    except Exception as e:
        return []
    

  

@router.get('/dashboard-static-cards/{category}/{date}', status_code=status.HTTP_200_OK)
async def fill_static_cards(date: str, category: str, db: Session = Depends(get_db)):
    """
    Retrieve static card metrics for the dashboard.
    """
    print(f"\n \n \n Static Card Log")
    # Define dynamic filters
    category_filters = {
        "All": "1=1",
        "JRE episodes": "jre_episode = true AND mma_episode = false AND toon_episode = false",
        "JRE episodes 5+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 5000000",
        "JRE episodes 10+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 10000000",
        "MMA episodes": "mma_episode = true AND jre_episode = false AND toon_episode = false",
        "Toon episodes": "toon_episode = true AND jre_episode = false AND mma_episode = false",
        "Other": "jre_episode = false AND mma_episode = false AND toon_episode = false",
    }

    # Get category filter safely
    category_filter = category_filters.get(category, "1=1")

    # SQL Query with the selected filters
    query = text(f"""
        WITH UNNESTED AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, UNNEST(video_stats) AS video_stats
            FROM jre_insights_table
            WHERE extraction_date = :date
        ),
        UNNESTED_COLUMNS AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, (video_stats:: video_stats).*
            FROM UNNESTED
        ),
        AGGREGATION AS (
            SELECT 
                COUNT(*) AS total_count,		
                SUM(CASE WHEN jre_episode = true THEN 1 ELSE 0 END) AS jre_videos_count,
                SUM(CASE WHEN mma_episode = true THEN 1 ELSE 0 END) AS mma_videos_count,
                SUM(CASE WHEN toon_episode = true THEN 1 ELSE 0 END) AS toon_episode_count,
                SUM(CASE WHEN toon_episode = false AND mma_episode = false AND jre_episode = false THEN 1 ELSE 0 END) AS other_episodes_count,
                -- Duration
                SUM(duration_in_seconds/60) AS total_duration,
                SUM(CASE WHEN jre_episode = true THEN (duration_in_seconds/60) ELSE 0 END) AS jre_videos_duration,
                SUM(CASE WHEN mma_episode = true THEN (duration_in_seconds/60) ELSE 0 END) AS mma_videos_duration,
                SUM(CASE WHEN toon_episode = true THEN (duration_in_seconds/60) ELSE 0 END) AS toon_episode_duration,
                SUM(CASE WHEN toon_episode = false AND mma_episode = false AND jre_episode = false THEN (duration_in_seconds/60) ELSE 0 END) AS other_episode_duration,
                -- Views
                SUM(view_count) AS total_views,
                SUM(CASE WHEN jre_episode = true THEN view_count ELSE 0 END) AS jre_videos_views,
                SUM(CASE WHEN mma_episode = true THEN view_count ELSE 0 END) AS mma_videos_views,
                SUM(CASE WHEN toon_episode = true THEN view_count ELSE 0 END) AS toon_episode_views,
                SUM(CASE WHEN toon_episode = false AND mma_episode = false AND jre_episode = false THEN view_count ELSE 0 END) AS other_episode_views
            FROM UNNESTED_COLUMNS
            WHERE
            extraction_date = :date
            AND {category_filter}
        )
        SELECT *
        FROM AGGREGATION;
        """
    )

    try:
        # Execute the query and fetch results
        results = db.execute(query, {"date": date}).fetchone()

        # Ensure the results are properly mapped (access via index)
        if results:
            response_data = {
                "total_count": results[0],
                "jre_videos_count": results[1],
                "mma_videos_count": results[2],
                "toon_episode_count": results[3],
                "other_episodes_count": results[4],

                "total_duration": results[5],
                "jre_videos_duration": results[6],
                "mma_videos_duration": results[7],
                "toon_episode_duration": results[8],
                "other_episode_duration": results[9],

                "total_views": results[10],
                "jre_videos_views": results[11],
                "mma_videos_views": results[12],
                "toon_episode_views": results[13],
                "other_episodes_views": results[14],
            }
        else:
            response_data = {}

        return response_data

    except Exception as e:
        print("Database error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data."
        )

@router.get('/dashboard-special-cards/{category}/{date}', status_code=status.HTTP_200_OK)
async def fill_special_cards(date: str, category: str, db: Session = Depends(get_db)):
    """
    Retrieve metrics for new views and likes based on the provided category and date.
    """
    try:
        # Calculate the previous day's date
        yesterday_query = text(f"""
        SELECT DISTINCT extraction_date AS yesterday_date
        FROM jre_insights_table
        WHERE extraction_date < :date 
        ORDER BY extraction_date DESC
        LIMIT 1;
        """)
        
        yesterday_date = db.execute(yesterday_query, {"date": date}).fetchone()
        print(yesterday_date)
        #convert yesterday_date to string
        yesterday_date = yesterday_date[0].strftime("%Y-%m-%d")
        #yesterday_date = (date_object - timedelta(days=1)).strftime("%Y-%m-%d")

        # Define category filters
        category_filters = {
            "All": "1=1",
            "JRE episodes": "jre_episode = true AND mma_episode = false AND toon_episode = false",
            "JRE episodes 5+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 5000000",
            "JRE episodes 10+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 10000000",
            "MMA episodes": "mma_episode = true AND jre_episode = false AND toon_episode = false",
            "Toon episodes": "toon_episode = true AND jre_episode = false AND mma_episode = false",
            "Other": "jre_episode = false AND mma_episode = false AND toon_episode = false",
        }

        # Get the filter for the category
        category_filter = category_filters.get(category, "1=1")

        # SQL Query with dynamic dates and category filter
        query = text(f"""
        WITH UNNESTED_yesterday AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, UNNEST(video_stats) AS video_stats
            FROM jre_insights_table
            WHERE extraction_date = :yesterday_date
        ),
        UNNESTED_today AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, UNNEST(video_stats) AS video_stats
            FROM jre_insights_table
            WHERE extraction_date = :today_date
        ),
        UNNESTED_COLUMNS_yesterday AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, (video_stats:: video_stats).*
            FROM UNNESTED_yesterday
        ),
        UNNESTED_COLUMNS_today AS (
            SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, (video_stats:: video_stats).*
            FROM UNNESTED_today
        ),
        AGGREGATION_today AS (
            SELECT 
                SUM(view_count) AS total_views_today,
                SUM(like_count) AS total_likes_today
            FROM UNNESTED_COLUMNS_today
            WHERE extraction_date = :today_date
            AND {category_filter}
        ),
        AGGREGATION_yesterday AS (
            SELECT 
                SUM(view_count) AS total_views_yesterday,
                SUM(like_count) AS total_likes_yesterday
            FROM UNNESTED_COLUMNS_yesterday
            WHERE extraction_date = :yesterday_date 
            AND {category_filter}
        )
        SELECT  
            COALESCE(total_views_today, 0) - COALESCE(total_views_yesterday, 0) AS new_views,
            COALESCE(total_likes_today, 0) - COALESCE(total_likes_yesterday, 0) AS new_likes
        FROM AGGREGATION_today, AGGREGATION_yesterday;
        """)

        # Execute the query with parameters
        results = db.execute(query, {"today_date": date, "yesterday_date": yesterday_date}).fetchone()

        # Process the results
        if results:
            response_data = {
                "new_views": results[0],
                "new_likes": results[1],
            }
        else:
            response_data = {
                "new_views": 0,
                "new_likes": 0,
            }

        return response_data

    except Exception as e:
        print("Error fetching special card data:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data."
        )

"""
Router to get the dashboard chart based on category and date
"""
@router.get('/dashboard-graph/{category}/{date}', status_code=status.HTTP_200_OK)
async def get_dashboard_chart(date: str, category: str, db: Session = Depends(get_db)):
    """
    Fetch dashboard data based on the selected date and category.
    """
    try:
        # Define dynamic filters
        category_filters = {
            "All": "1=1",
            "JRE episodes": "jre_episode = true AND mma_episode = false AND toon_episode = false",
            "JRE episodes 5+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 5000000",
            "JRE episodes 10+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 10000000",
            "MMA episodes": "mma_episode = true AND jre_episode = false AND toon_episode = false",
            "Toon episodes": "toon_episode = true AND jre_episode = false AND mma_episode = false",
            "Other": "jre_episode = false AND mma_episode = false AND toon_episode = false",
        }

        category_filter = category_filters.get(category, "1=1")

        # Define the SQL query with parameter placeholders
        query = text(f"""
        WITH UNNESTED AS (
            SELECT 
                title, 
                publish_date, 
                jre_episode, 
                mma_episode, 
                toon_episode, 
                duration_in_seconds, 
                UNNEST(video_stats) AS video_stats
            FROM jre_insights_table
            WHERE extraction_date = :date
        ),
        UNNESTED_COLUMNS AS (
            SELECT 
                title, 
                publish_date, 
                jre_episode, 
                mma_episode, 
                toon_episode, 
                duration_in_seconds, 
                (video_stats::video_stats).*
            FROM UNNESTED
        )
        SELECT 
            title, 
            view_count, 
            duration_in_seconds, 
            like_count, 
            publish_date
        FROM UNNESTED_COLUMNS
        WHERE 
            extraction_date = :date
            AND {category_filter}
        ORDER BY publish_date ASC;
        """)

        # Execute the query with the `date` parameter
        results = db.execute(query, {"date": date}).fetchall()

        # Convert results to a JSON-serializable format
        data = [
            {
                "title": row.title,
                "publish_date": row.publish_date,
                "views": row.view_count,
                "likes": row.like_count,
                "duration_in_seconds": row.duration_in_seconds
            }
            for row in results
        ]

        return data
    except SQLAlchemyError as e:
        print("Database error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data."
        )
  
"""
Router to get the col-4 top 10 card 
"""
@router.get('/dashboard-top-10-card/{category}/{date}/{filterType}', status_code=status.HTTP_200_OK)
async def fill_special_cards(date: str, category: str, filterType: str, db: Session = Depends(get_db)):
    """
    Retrieve top 10 based on the provided category and date.
    """
    try:
        # Define category filters
        category_filters = {
            "All": "1=1",
            "JRE episodes": "jre_episode = true AND mma_episode = false AND toon_episode = false",
            "JRE episodes 5+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 5000000",
            "JRE episodes 10+ million views": "jre_episode = true AND mma_episode = false AND toon_episode = false AND view_count > 10000000",
            "MMA episodes": "mma_episode = true AND jre_episode = false AND toon_episode = false",
            "Toon episodes": "toon_episode = true AND jre_episode = false AND mma_episode = false",
            "Other": "jre_episode = false AND mma_episode = false AND toon_episode = false",
        }

        # Get the filter for the category
        category_filter = category_filters.get(category, "1=1")    
        if filterType == 'watchedVideos':
            query = text(f"""
            WITH UNNESTED AS (
                SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, UNNEST(video_stats) AS video_stats
                FROM jre_insights_table
                WHERE extraction_date = :date
            ),
            UNNESTED_COLUMNS AS (
                SELECT title, publish_date, jre_episode, mma_episode, toon_episode, duration_in_seconds, (video_stats:: video_stats).*
                FROM UNNESTED
            )
            SELECT title, view_count
            FROM UNNESTED_COLUMNS
            WHERE extraction_date = :date
            AND {category_filter}
            ORDER BY view_count DESC
            LIMIT 10;
            """)
            # Execute the query with the `date` parameter
            results = db.execute(query, {"date": date}).fetchall()

            response_data = [{"title": row.title, "view_count": row.view_count} for row in results]
            return response_data
        else:
            query = text(f"""
            WITH UNNESTED AS (
                SELECT title, guest_name, jre_episode, mma_episode, toon_episode, duration_in_seconds, UNNEST(video_stats) AS video_stats
                FROM jre_insights_table
                WHERE extraction_date = :date
            ),
            UNNESTED_COLUMNS AS (
                SELECT title, guest_name, jre_episode, mma_episode, toon_episode, duration_in_seconds, (video_stats:: video_stats).*
                FROM UNNESTED
            ),
            GUESTS AS(
            SELECT title, guest_name, jre_episode, mma_episode, toon_episode, duration_in_seconds, view_count
            FROM UNNESTED_COLUMNS 
            WHERE extraction_date = :date AND guest_name <> '-' AND guest_name <> '' AND guest_name <> 'Fight Companion'
            AND {category_filter}
            GROUP BY title, guest_name, jre_episode, mma_episode, toon_episode, duration_in_seconds, view_count
            )
            SELECT guest_name, COUNT(1) AS appearances
            FROM GUESTS 
            GROUP BY guest_name
            ORDER BY COUNT(1) DESC
            LIMIT 10
            """)
            # Execute the query with the `date` parameter
            results = db.execute(query, {"date": date}).fetchall()

            response_data = [{"guest_name": row.guest_name, "appearances": row.appearances} for row in results]
            return response_data

    except Exception as e:
        print("Error fetching special card data:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data."
        )