import java.util.*;

public class Main {

    static class Point implements Comparable<Point> {
        double x, y;

        Point(double x, double y) {
            this.x = x;
            this.y = y;
        }

        public int compareTo(Point p) {
            if (this.x != p.x)
                return Double.compare(this.x, p.x);
            return Double.compare(this.y, p.y);
        }

        public String toString() {
            return "(" + x + ", " + y + ")";
        }
    }

    static double crossProduct(Point a, Point b, Point c) {
        return (b.x - a.x) * (c.y - a.y)
                - (b.y - a.y) * (c.x - a.x);
    }

    static List<Point> convexHull(List<Point> points) {
        List<Point> sorted = new ArrayList<>(points);
        Collections.sort(sorted);

        if (sorted.size() <= 1)
            return sorted;

        List<Point> lower = new ArrayList<>();

        for (Point p : sorted) {
            while (lower.size() >= 2 &&
                    crossProduct(lower.get(lower.size() - 2),
                            lower.get(lower.size() - 1), p) <= 0) {
                lower.remove(lower.size() - 1);
            }
            lower.add(p);
        }

        List<Point> upper = new ArrayList<>();

        for (int i = sorted.size() - 1; i >= 0; i--) {
            Point p = sorted.get(i);

            while (upper.size() >= 2 &&
                    crossProduct(upper.get(upper.size() - 2),
                            upper.get(upper.size() - 1), p) <= 0) {
                upper.remove(upper.size() - 1);
            }
            upper.add(p);
        }

        lower.remove(lower.size() - 1);
        upper.remove(upper.size() - 1);

        lower.addAll(upper);

        return lower;
    }

    static boolean isInside(List<Point> polygon, Point p) {
        if (polygon.size() < 3)
            return false;

        int sign = 0;

        for (int i = 0; i < polygon.size(); i++) {
            Point a = polygon.get(i);
            Point b = polygon.get((i + 1) % polygon.size());

            double cross = crossProduct(a, b, p);

            if (Math.abs(cross) < 1e-9)
                continue;

            int currentSign = cross > 0 ? 1 : -1;

            if (sign == 0) {
                sign = currentSign;
            } else if (sign != currentSign) {
                return false;
            }
        }

        return true;
    }

    static double distance(Point a, Point b) {
        double dx = a.x - b.x;
        double dy = a.y - b.y;

        return Math.sqrt(dx * dx + dy * dy);
    }

    static List<Point> findInsideStars(List<Point> polygon,
            List<Point> stars) {
        List<Point> insideStars = new ArrayList<>();

        for (Point star : stars) {
            if (isInside(polygon, star)) {
                insideStars.add(star);
            }
        }

        return insideStars;
    }

    static Point[] findNearestCity(Point star, List<Point> cities) {
        Point nearestCity = null;
        double minDistance = Double.MAX_VALUE;

        for (Point city : cities) {
            double d = distance(star, city);

            if (d < minDistance) {
                minDistance = d;
                nearestCity = city;
            }
        }

        return new Point[] { nearestCity, new Point(minDistance, 0) };
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of cities: ");
        int n = sc.nextInt();

        List<Point> cities = new ArrayList<>();

        System.out.println("Enter city coordinates (x y):");

        for (int i = 0; i < n; i++) {
            double x = sc.nextDouble();
            double y = sc.nextDouble();

            cities.add(new Point(x, y));
        }

        System.out.print("Enter number of stars: ");
        int m = sc.nextInt();

        List<Point> stars = new ArrayList<>();

        System.out.println("Enter star coordinates (x y):");

        for (int i = 0; i < m; i++) {
            double x = sc.nextDouble();
            double y = sc.nextDouble();

            stars.add(new Point(x, y));
        }

        List<Point> polygon = convexHull(cities);

        System.out.println("\nConvex Hull Polygon:");

        for (Point p : polygon) {
            System.out.println(p);
        }

        List<Point> insideStars = findInsideStars(polygon, stars);

        System.out.println("\nStars lying inside the polygon:");

        if (insideStars.isEmpty()) {
            System.out.println("No stars lie inside the polygon.");
            sc.close();
            return;
        }

        for (Point star : insideStars) {
            System.out.println(star);
        }

        Random random = new Random();

        Point selectedStar = insideStars.get(random.nextInt(insideStars.size()));

        System.out.println("\nRandomly selected star:");
        System.out.println(selectedStar);

        Point nearestCity = null;
        double minDistance = Double.MAX_VALUE;

        System.out.println("\nDistances from selected star to cities:");

        for (Point city : cities) {
            double d = distance(selectedStar, city);

            System.out.println(
                    "Star " + selectedStar +
                            " to City " + city +
                            " = " + d);

            if (d < minDistance) {
                minDistance = d;
                nearestCity = city;
            }
        }

        System.out.println("\nNearest city:");
        System.out.println(nearestCity);

        System.out.println("\nMinimum Euclidean distance:");
        System.out.printf("%.2f%n", minDistance);

        sc.close();
    }
}