
from data_collection.data_collection import main as data_collection_main
from feature_engineering.feature_engineering import main as feature_engineering_main
from model_development.model_development import main as model_development_main
from evaluation.backtesting_framework import main as backtesting_main
from evaluation.performance_monitoring import main as performance_monitoring_main
from real_time_processing.real_time_odds_update import main as real_time_update_main
from real_time_processing.live_data_testing import main as live_data_testing_main

def main():
    # Data Collection
    data_collection_main()

    # Feature Engineering
    feature_engineering_main()

    # Model Development
    model_development_main()

    # Backtesting
    backtesting_main()

    # Performance Monitoring
    performance_monitoring_main()

    # Real-Time Processing
    real_time_update_main()
    live_data_testing_main()

if __name__ == "__main__":
    main()
