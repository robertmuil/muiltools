class Person
{
	public:
		Person(const std::string& fn, const std::string& ln)
			: first(fn), last(ln)
		{
		}
		std::string toString();

	private:
		std::string first;
		std::string last;

		friend std::ostream& operator<<(std::ostream& os, const Person& p)
		{
			return os << p.last << ", " << p.first;
		}

};
