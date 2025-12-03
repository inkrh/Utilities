using System;
using Xamarin.Forms;

namespace QualityReporter
{
	public class Ticker : StackLayout
	{
		Label contentLabel;
		string _content { get; set; } 

		public bool On { get; set; }

		public String Content
		{
			get
			{
				return _content;
			}
			set
			{
				if (!string.IsNullOrEmpty(value))
				{
					_content = value.Replace("\n", " ");
					contentLabel.Text = _content;

				}
			}
		}
		
		public Ticker()
		{
			contentLabel = new Label
			{
				TextColor = Color.White,
				VerticalOptions = LayoutOptions.End,
				HorizontalOptions = LayoutOptions.CenterAndExpand,
			};
			IsVisible = false;
			BackgroundColor = Color.FromHex("424242");
			Children.Add(contentLabel);
		}

		public void Run()
		{
			IsVisible = true;
			On = true;
			Device.StartTimer(new TimeSpan(0, 0, 0, 0, 20), () =>
			{
				if (!string.IsNullOrEmpty(Content))
				{
					Content = Content.Substring(1) + Content.Substring(0, 1);
				}
				else {
					On = false;
				}
				return On;
			});
		}
	}
}
