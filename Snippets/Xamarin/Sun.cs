using System;

using Xamarin.Forms;

namespace QualityReporter
{
	public class Sun : ContentView
	{
		Image sun;
		Image cloud;

		public bool On { get; set; }
		Grid contentGrid;

		public Sun()
		{
			currentPadding = -75;

			sun = new Image { Source = "sun.png", WidthRequest = 75, HeightRequest = 42, VerticalOptions = LayoutOptions.Center, HorizontalOptions = LayoutOptions.Center };
			cloud = new Image { Source = "cloud.png", WidthRequest = 75, HeightRequest = 42, VerticalOptions = LayoutOptions.Center, HorizontalOptions = LayoutOptions.Center, IsVisible=false };

			contentGrid = new Grid
			{
				HorizontalOptions = LayoutOptions.Start,
				VerticalOptions = LayoutOptions.Start,
				WidthRequest = 75,
				HeightRequest = 42,
				BackgroundColor = Color.Transparent,
				Children = { sun,cloud },
				Margin = new Thickness(currentPadding, 0, DeviceDetails.Width-currentPadding-75,0)
			};

			Content = contentGrid;


		}

		double currentPadding { get; set; }

		public void Run()
		{
			On = true;
			Device.StartTimer(new TimeSpan(0, 0, 0, 0, 10), () =>
			{
				currentPadding += 1;
				if (currentPadding > DeviceDetails.Width + 75)
				{
					currentPadding = 0;
					sun.IsVisible = !sun.IsVisible;
					cloud.IsVisible = !cloud.IsVisible;

				}
				contentGrid.Margin = new Thickness(currentPadding, 0, DeviceDetails.Width - currentPadding - 75,0);
				return On;
			});
		}


	}
}

