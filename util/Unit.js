module.exports = class Unit
{
	secondsToDays(seconds)
	{
		seconds = parseInt(seconds);
		let days = seconds / (3600 * 8);;
		return Math.ceil(days);
	}

	durationToPrice(duration) // todo check
	{
		duration = parseInt(duration);
		let duration_hours = duration / 3600;
		let price = duration_hours * process.env.price_per_hour;
		let tax = price * process.env.tax_percent / 100;
		let sum = price + tax;
		return {
			price: price.toFixed(2),
			tax: tax.toFixed(2),
			sum: sum.toFixed(2)
		};
	}
}